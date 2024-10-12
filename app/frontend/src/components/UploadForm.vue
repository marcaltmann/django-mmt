<script setup lang="ts">
import InlineMessage from '@/components/InlineMessage.vue'

const ACCEPTED_FILES = 'video/*,audio/*,image/*,model/vnd.mts,application/mxf'
const FILESIZE_LIMIT = 1 * 1024 * 1024 * 1024 * 1024  // 1 TB

const { onFileChange } = defineProps<{
  loading: boolean,
  error: string | null,
  selectedFiles: Array<File>,
  onSubmit: (payload: Event) => void
  onFileChange: (files: Array<File>) => void
}>()

function handleFileChange(event: Event): void {
  const fileInput = event.target as HTMLInputElement
  const files = fileInput.files as FileList
  const fileList = [...files]
  onFileChange(fileList)
}

function resetForm(event: Event): void {
  onFileChange([])
}
</script>

<template>
  <InlineMessage v-if="error" type="error" class="u-mt">
    {{ $t(`${error}`) }}
  </InlineMessage>

  <form @submit="onSubmit" @reset="resetForm">
    <div class="u-mt">
      <label for="file-input" class="form__label">
        {{ $t('components.UploadButton.label') }}
      </label>
      <div class="control">
        <input
          class="upload-button__input u-mt-1/2"
          type="file"
          name="files"
          id="file-input"
          :accept="ACCEPTED_FILES"
          multiple
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
        {{ $t('components.UploadForm.title') }}
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
      <label class="form__label u-ml-1/4" htmlFor="make_available_on_platform">
        {{ $t('components.UploadForm.makeAvailableOnPlatform') }}
      </label>
    </div>

    <div class="u-mt-1/2">
      <input
        name="transcribe"
        type="checkbox"
        class="form__input"
        id="transcribe"
      />
      <label class="form__label u-ml-1/4" htmlFor="transcribe">
        {{ $t('components.UploadForm.transcribe') }}
      </label>
    </div>

    <div class="u-mt-1/2">
      <input
        name="check_media_files"
        type="checkbox"
        class="form__input"
        id="check_media_files"
      />
      <label class="form__label u-ml-1/4" htmlFor="check_media_files">
        {{ $t('components.UploadForm.checkMediaFiles') }}
      </label>
    </div>

    <div class="u-mt-1/2">
      <input
        name="replace_existing_files"
        type="checkbox"
        class="form__input"
        id="replace_existing_files"
      />
      <label class="form__label u-ml-1/4" htmlFor="replace_existing_files">
        {{ $t('components.UploadForm.replaceExistingFiles') }}
      </label>
    </div>

    <div class="field u-mt">
      <button type="submit" class="form__button" :disabled="loading">
        {{ $t('components.UploadForm.submit') }}
      </button>

      <button type="reset"
        class="form__button form__button--secondary u-ml-1/2">
        {{ $t('components.UploadForm.reset') }}
      </button>
    </div>
  </form>
</template>
