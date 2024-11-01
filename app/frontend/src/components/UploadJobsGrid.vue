<script setup lang="ts">
import { useI18n } from 'vue-i18n'

import UploadJobCard from './UploadJobCard.vue';
import type { UploadJob } from '@/types'

const { t } = useI18n()

const props = defineProps<{
  uploadJobs: Array<UploadJob>
  loading: boolean
  onDelete: (uploadJobId: number, title: string) => Promise<void>
}>()
</script>

<template>
  <div class="grid">
    <UploadJobCard v-for="job in uploadJobs"
      :upload-job="job"
      :on-delete="onDelete" />
  </div>
</template>
