import CurrentUpload from './current_upload.js'
import UploadQueueItem from './upload_queue_item.js'
import FileStorage from './file_storage.js'
import getNextFileId from './get_next_file_id.js'
import addFile from "./add_file.js"
import registerUpload from "./register_upload.js"
import submitChecksum from "./submit_checksum.js"
import createChecksum from "./create_checksum.js"

let xhrRef = null;
const storedFiles = new FileStorage();

export default {
  components: {
    CurrentUpload,
    UploadQueueItem
  },
  props: ['files', 'currentUploadJobId'],
  data() {
    const files = this.files || [];
    return {
      pending: files.map(file => {
        const id = getNextFileId();
        storedFiles.storeFile(id, file);
        return {
          jobId: id,
          filename: file.name,
          filesize: file.size,
        };
      }),
      active: null,
    };
  },
  mounted() {
    this.startNextJob();
  },
  computed: {
    itemCount() {
      let result = this.pending.length;
      if (this.active) {
        result += 1;
      }
      return result;
    },
    isEmpty() {
      return this.itemCount === 0;
    },
  },
  methods: {
    removeActive() {
      const activeJob = this.active;
      if (activeJob) {
        storedFiles.removeFile(activeJob.jobId);
      }
      this.active = null;
    },
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
    },
    async startNextJob() {
      if (this.pending.length === 0) {
        /* Queue is empty, job done. */
        /* TODO: Redirect or call callback */
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
    },
  },
  template: `
    <ul>
      <CurrentUpload v-if="active" :upload="active" />
      <UploadQueueItem v-for="job in pending" :key="job.jobId" :upload="job" />
    </ul>
  `
}
