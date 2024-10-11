<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import useSWRV from 'swrv'

import { fetchWrapper } from '@/helpers/fetch-wrapper'
import UploadsTable from '@/components/UploadsTable.vue'
import InlineMessage from '@/components/InlineMessage.vue'
import truncateText from '@/helpers/truncate-text'

const baseUrl = import.meta.env.VITE_API_URL

const { t } = useI18n()

const { data, error, isValidating } = useSWRV(`${baseUrl}/uploads/`, fetchWrapper.get)

async function handleDeleteClick(uploadId: number, filename: string) {
  const confirmed = confirm(
    t('views.UploadsView.confirmDelete', { filename: truncateText(filename, 20) })
  )

  if (!confirmed) {
    return
  }

  await fetchWrapper.post(`${baseUrl}/uploads/${uploadId}/delete/`)
}

</script>

<template>
  <main class="container u-mt u-mb-2">
    <h2>
      {{ $t('views.UploadsView.title') }}
    </h2>

    <InlineMessage v-if="error" type="error" class="u-mt">
      {{ $t(`${error.message}`) }}
    </InlineMessage>

    <UploadsTable
      v-if="data"
      class="u-mt"
      :uploads="data"
      :loading="isValidating"
      :on-delete="handleDeleteClick"
    />
  </main>
</template>
