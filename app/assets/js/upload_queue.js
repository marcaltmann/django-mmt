import getNextFileId from "./get_next_file_id"
import addFile from "./add_file.js"
import registerUpload from "./register_upload.js"
import submitChecksum from "./submit_checksum.js"
import createChecksum from "./create_checksum.js"
import FileStorage from "./file_storage.js"

export default class UploadQueue {
  constructor(files, uploadJobId) {
    this.storedFiles = new FileStorage();
    this.xhrRef = null;
    this.currentUploadJobId = uploadJobId;
    this.active = null;
    this.pending = files.map(file => {
      const id = getNextFileId();
      this.storedFiles.storeFile(id, file);
      return {
        jobId: id,
        filename: file.name,
        filesize: file.size,
      };
    });
    this.startNextJob();
  }

  itemCount() {
    let result = this.pending.length;
    if (this.active) {
      result += 1;
    }
    return result;
  }

  percentageFile() {
    if (!this.active) {
      return 0;
    }
    return (this.active.transferred / this.active.filesize) * 100;
  }

  percentageChecksum() {
    if (!this.active) {
      return 0;
    }
    return (this.active.checksumProgress / 1) * 100;
  }

  isEmpty() {
    return this.itemCount() === 0;
  }

  // Actions
  addJobsFromFiles(files, uploadJobId) {

  }

  removeActive() {
    const activeJob = this.active;
    if (activeJob) {
      this.storedFiles.removeFile(activeJob.jobId);
    }
    this.active = null;
  }

  removeJob(idToRemove) {
    const index = this.pending.findIndex(
      upload => upload.jobId === idToRemove
    );
    if (index === -1) {
      return;
    }
    const firstPart = this.pending.slice(0, index);
    const lastPart = this.pending.slice(index + 1);
    this.pending = firstPart.concat(lastPart);
  }

  async startNextJob() {
    if (this.pending.length === 0) {
      /* Queue is empty, job done. */
      this.currentUploadJobId = null;
      return;
    }

    if (this.active || !this.currentUploadJobId) {
      /* This should never be reached. */
      return;
    }

    const nextJob = this.pending[0];
    const nextJobId = nextJob.jobId;
    const nextJobFile = this.storedFiles.getFile(nextJobId);

    const registeredUpload = await registerUpload(
      nextJobFile,
      this.currentUploadJobId
    );
    if (!registeredUpload) {
      // Something did not work during upload registration
      return;
    }

    const registeredJob = {
      jobId: nextJobId,
      serverId: registeredUpload.id,
      serverFilename: registeredUpload.filename,
      filesize: nextJobFile.size,
      transferred: 0,
      checksumProgress: 0,
      startedAt: new Date()
    };

    this.active = registeredJob;
    this.pending = this.pending.slice(1);

    const request = addFile({
      fileId: registeredJob.serverId,
      file: nextJobFile,
      filename: registeredJob.serverFilename,
      onProgress: updatedTransferredValue => {
        if (this.active) {
          this.active = {
            ...this.active,
            transferred: updatedTransferredValue
          };
        }
      },
      onEnd: () => {
        this.active = null;
        this.startNextJob();
        this.xhrRef = null;
      },
      onAbort: () => {
        // onEnd will also catch aborted uploads.
        console.log("onAbort executed");
      }
    })
    this.xhrRef = request;

    const checksum = await createChecksum(nextJobFile, progress => {
      if (this.active) {
        this.active = {
          ...this.active,
          checksumProgress: progress,
        };
      }
    })
    // Set checksum progress to 100% after checksum is calculated.
    if (this.active) {
      this.active = {
        ...this.active,
        checksumProgress: 1,
      };
    }

    const result = await submitChecksum(registeredJob.serverId, checksum);
  }
}
