<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { useI18n } from 'vue-i18n'
import useSWRV from 'swrv'

import { useQueueStore } from '@/stores/queue'
import { fetchWrapper } from '@/helpers/fetch-wrapper'
import UploadForm from '@/components/UploadForm.vue'
import InlineMessage from '@/components/InlineMessage.vue'

const baseUrl = import.meta.env.VITE_API_URL
const store = useQueueStore()

const selectedFiles: Ref<Array<File>> = ref([])

async function handleButtonClick(e: Event) {
  const fileInput = e.target as HTMLInputElement
  const files = fileInput.files as FileList
  const fileList = [...files]

  selectedFiles.value = fileList

  console.log(fileList)
  return;

  store.addJobsFromFiles(fileList)
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
      :on-change="handleButtonClick"
      :selected-files="selectedFiles"
      class="u-mt"
    />
  </main>
</template>
