import { fetchWrapper } from '../fetch_wrapper.js'
import InlineMessage from './inline_message.js'
import UploadQueue from './upload_queue.js'

const FILESIZE_LIMIT = 1 * 1024 * 1024 * 1024 * 1024  // 1 TB


export default {
  components: {
    UploadQueue,
    InlineMessage,
  },
  props: ['csrf-token'],
  data() {
    return {
      selectedFiles: [],
      error: false,
      loading: false,
      uploadJob: null,
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFiles = [...event.target.files];
    },
    async handleSubmit(event) {
      event.preventDefault();
      const form = event.target;
      const elements = form.elements;

      const titleInput = elements[1];
      const descriptionElem = elements[2] ;
      const languageInput = elements[3];
      const makeAvailableOnPlatformCheckbox = elements[4];
      const transcribeCheckbox = elements[5];
      const checkMediaFilesCheckbox = elements[6];
      const replaceExistingFilesCheckbox = elements[7];

      const title = titleInput.value.trim();
      const description = descriptionElem.value.trim();
      const language = languageInput.value.trim();
      const makeAvailableOnPlatform = makeAvailableOnPlatformCheckbox.checked;
      const transcribe = transcribeCheckbox.checked;
      const checkMediaFiles = checkMediaFilesCheckbox.checked;
      const replaceExistingFiles = replaceExistingFilesCheckbox.checked;

      this.error = null;
      this.loading = true;

      const result = await fetchWrapper
        .post(`/${this.$i18n.locale}/upload-jobs/create/`, {
          title,
          description,
          language,
          make_available_on_platform: makeAvailableOnPlatform,
          transcribe,
          check_media_files: checkMediaFiles,
          replace_existing_files: replaceExistingFiles,
        })
        .catch((err) => {
          this.error = err.message;
          console.log(err);
          return null;
        });

      this.loading = false;
      this.uploadJob = result;
    },
    resetForm() {
      this.selectedFiles = [];
    },
  },
  template: `
    <UploadQueue v-if="uploadJob" :files="selectedFiles"
                 :current-upload-job-id="uploadJob.id" />
  `
}
