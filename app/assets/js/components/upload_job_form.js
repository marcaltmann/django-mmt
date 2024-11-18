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
        .post(`/${this.$i18n.locale}/upload-jobs/create/}`, {
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
    <InlineMessage v-if="error" type="error" class="u-mt">
      {{ $t(error) }}
    </InlineMessage>
  
    <form @submit="handleSubmit" @reset="resetForm">
      <div class="u-mt">
        <label for="file-input" class="form__label">
          {{ $t('components.UploadButton.label') }}*
        </label>
        <div class="control">
          <input
            class="upload-button__input u-mt-small"
            type="file"
            name="files"
            id="file-input"
            accept="video/*,audio/*,image/*,model/vnd.mts,application/mxf"
            multiple
            required
            @change="handleFileChange"
          />
        </div>
      </div>
  
      <ul v-if="selectedFiles.length > 1" class="u-mt">
        <li v-for="file in selectedFiles">
          {{ file.name }}
        </li>
      </ul>
  
      <div class="u-mt">
        <label class="form__label" htmlFor="username">
          {{ $t('components.UploadForm.title') }}*
        </label>
        <div class="control">
          <input
            id="title"
            name="title"
            type="text"
            required
            class="form__input"
          />
        </div>
      </div>
  
      <div class="u-mt">
        <label class="form__label" htmlFor="description">
          {{ $t('components.UploadForm.description') }}
        </label>
        <div class="control">
          <textarea
            name="description"
            class="form__input"
            id="description"
          ></textarea>
        </div>
      </div>
  
      <div class="u-mt">
        <label class="form__label" htmlFor="languages">
          {{ $t('components.UploadForm.language') }}
        </label>
        <div class="control">
          <input
            name="languages"
            type="text"
            class="form__input"
            id="languages"
          />
        </div>
      </div>
  
      <div class="u-mt">
        <input
          name="make_available_on_platform"
          type="checkbox"
          class="form__input"
          id="make_available_on_platform"
        />
        <label class="form__label u-ml-tiny" htmlFor="make_available_on_platform">
          {{ $t('components.UploadForm.makeAvailableOnPlatform') }}
        </label>
      </div>
  
      <div class="u-mt-small">
        <input
          name="transcribe"
          type="checkbox"
          class="form__input"
          id="transcribe"
        />
        <label class="form__label u-ml-tiny" htmlFor="transcribe">
          {{ $t('components.UploadForm.transcribe') }}
        </label>
      </div>
  
      <div class="u-mt-small">
        <input
          name="check_media_files"
          type="checkbox"
          class="form__input"
          id="check_media_files"
        />
        <label class="form__label u-ml-tiny" htmlFor="check_media_files">
          {{ $t('components.UploadForm.checkMediaFiles') }}
        </label>
      </div>
  
      <div class="u-mt-small">
        <input
          name="replace_existing_files"
          type="checkbox"
          class="form__input"
          id="replace_existing_files"
        />
        <label class="form__label u-ml-tiny" htmlFor="replace_existing_files">
          {{ $t('components.UploadForm.replaceExistingFiles') }}
        </label>
      </div>
  
      <div class="field u-mt">
        <button type="submit" class="form__button" :disabled="loading">
          {{ $t('components.UploadForm.submit') }}
        </button>
  
        <button type="reset"
          class="form__button form__button--secondary u-ml-small">
          {{ $t('components.UploadForm.reset') }}
        </button>
      </div>
    </form>

    <UploadQueue v-if="uploadJob" :files="selectedFiles"
                 :current-upload-job-id="uploadJob.id" />
  `
}
