<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useI18n } from 'vue-i18n'
import useSWRV from 'swrv'

import { useQueueStore } from '@/stores/queue'
import { fetchWrapper } from '@/helpers/fetch-wrapper'
import UploadForm from '@/components/UploadForm.vue'
import InlineMessage from '@/components/InlineMessage.vue'
import type { UploadJob } from '@/types'

const baseUrl = import.meta.env.VITE_API_URL

const store = useQueueStore()

const selectedFiles: Ref<Array<File>> = ref([])
const loading = ref(false)
const error: Ref<string | null> = ref(null)
const uploadJob: Ref<UploadJob | null> = ref(null)

async function updateFiles(files: Array<File>): void {
  console.log(files)
  selectedFiles.value = files
  return;

  store.addJobsFromFiles(files)
}

async function handleSubmit(event: Event): Promise<void> {
  event.preventDefault()
  const form = event?.target as HTMLFormElement
  const elements = form.elements

  const titleInput = elements[1] as HTMLInputElement
  const descriptionElem = elements[2] as HTMLTextAreaElement
  const languageInput = elements[3] as HTMLInputElement
  const makeAvailableOnPlatformCheckbox = elements[4] as HTMLInputElement
  const transcribeCheckbox = elements[5] as HTMLInputElement
  const checkMediaFilesCheckbox = elements[6] as HTMLInputElement
  const replaceExistingFilesCheckbox = elements[7] as HTMLInputElement

  const title = titleInput.value.trim()
  const description = descriptionElem.value.trim()
  const language = languageInput.value.trim()
  const makeAvailableOnPlatform = makeAvailableOnPlatformCheckbox.checked
  const transcribe = transcribeCheckbox.checked
  const checkMediaFiles = checkMediaFilesCheckbox.checked
  const replaceExistingFiles = replaceExistingFilesCheckbox.checked

  error.value = null
  loading.value = true

  const result = await fetchWrapper
    .post(`${baseUrl}/uploads/create/`, {
      title,
      description,
      language,
      make_available_on_platform: makeAvailableOnPlatform,
      transcribe,
      check_media_files: checkMediaFiles,
      replace_existing_files: replaceExistingFiles,
    })
    .catch((err) => {
      error.value = err
      console.log(err)
      return null
    })
  loading.value = false

  if (result) {
    uploadJob.value = result
    console.log(uploadJob.value)
  }

  // store.addJobsFromFiles(selectedFiles.value)
}
</script>

<template>
  <main class="container u-mt u-mb-2">
    <h2>
      {{ $t('views.NewUploadView.title') }}
    </h2>

    <InlineMessage v-if="error" type="error" class="u-mt">
      {{ $t(`${error.message}`) }}
    </InlineMessage>

    <UploadForm
      :selected-files="selectedFiles"
      :on-file-change="updateFiles"
      :on-submit="handleSubmit"
      class="u-mt"
    />
  </main>
</template>
