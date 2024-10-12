<script setup lang="ts">
import { watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink, useRoute } from 'vue-router'
import useSWRV from 'swrv'

import { fetchWrapper } from '@/helpers/fetch-wrapper'
import UploadedFilesTable from '@/components/UploadedFilesTable.vue'
import InlineMessage from '@/components/InlineMessage.vue'
import truncateText from '@/helpers/truncate-text'

const baseUrl = import.meta.env.VITE_API_URL
const route = useRoute()
const { t } = useI18n()

const { data, error, isValidating } = useSWRV(`${baseUrl}/uploads/${route.params.id}`,
  fetchWrapper.get)

async function handleDeleteClick(uploadId: number, filename: string) {
  const confirmed = confirm(
    t('views.UploadJobDetailView.confirmDelete', { filename: truncateText(filename, 20) })
  )

  if (!confirmed) {
    return
  }

  await fetchWrapper.post(`${baseUrl}/uploads/${uploadId}/delete/`)
}

</script>

<template>
  <main class="container u-mt u-mb-2">
    <nav class="breadcrumbs">
      <p>
        <RouterLink class="breadcrumbs__link" to="/uploads">{{ $t('views.UploadJobDetailView.uploads') }}</RouterLink>
          ▸
        <a>
          {{ data?.title }}
        </a>
      </p>
    </nav>

    <h2 class="u-mt">
      {{ data?.title }}
    </h2>

    <InlineMessage v-if="error" type="error" class="u-mt">
      {{ $t(`${error.message}`) }}
    </InlineMessage>

    <p v-if="data" class="u-mt">
      {{ data.description }}
    </p>

    <UploadedFilesTable
      v-if="data"
      class="u-mt"
      :files="data.files"
      :loading="isValidating"
      :on-delete="handleDeleteClick"
    />
  </main>
</template>
