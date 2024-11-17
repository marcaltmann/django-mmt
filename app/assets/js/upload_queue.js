import getNextFileId from "./get_next_file_id"
import addFile from "./add_file.js"
import registerUpload from "./register_upload.js"
import submitChecksum from "./submit_checksum.js"
import createChecksum from "./create_checksum.js"
import FileStorage from "./file_storage.js"

const storedFiles = new FileStorage()
let xhrRef = null

export default class UploadQueue {
  constructor() {
    this.pending = [];
    this.active = null;
    this.currentUploadJobId = null;
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
    const newPendingUploads = files.map(file => {
      const id = getNextFileId();
      storedFiles.storeFile(id, file);
      return {
        jobId: id,
        filename: file.name,
        filesize: file.size,
      };
    })
    this.currentUploadJobId = uploadJobId;
    this.pending = this.pending.concat(newPendingUploads);
    if (!this.active) {
      this.startNextJob();
    }
  }

  removeActive() {
    const activeJob = this.active;
    if (activeJob) {
      storedFiles.removeFile(activeJob.jobId);
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
    const nextJobFile = storedFiles.getFile(nextJobId);

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
        xhrRef = null;
      },
      onAbort: () => {
        // onEnd will also catch aborted uploads.
        console.log("onAbort executed");
      }
    })
    xhrRef = request;

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
