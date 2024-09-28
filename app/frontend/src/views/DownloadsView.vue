<script setup lang="ts">
import useSWRV from 'swrv'

import { fetchWrapper } from '@/helpers/fetch-wrapper'
import InlineMessage from '@/components/InlineMessage.vue'
import DownloadsTable from '@/components/DownloadsTable.vue'

const baseUrl = `${import.meta.env.VITE_API_URL}`
const { data, error, isValidating } = useSWRV(`${baseUrl}/downloads/`, fetchWrapper.get)
</script>

<template>
  <main class="container u-mt u-mb-2">
    <h2>
      {{ $t('views.DownloadsView.title') }}
    </h2>

    <InlineMessage v-if="error" type="error" class="u-mt">
      {{ $t(`${error.message}`) }}
    </InlineMessage>

    <DownloadsTable
      v-if="data"
      class="u-mt"
      :downloads="data"
      :loading="isValidating"
    />
  </main>
</template>
