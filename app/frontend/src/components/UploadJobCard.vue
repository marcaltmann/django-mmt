<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'

import formatDate from '@/helpers/format-date'
import TrashIcon from '@/icons/TrashIcon.vue'
import type { UploadJob } from '@/types'

const { t } = useI18n()

const props = defineProps<{
  uploadJob: UploadJob
  onDelete: (uploadJobId: number, title: string) => Promise<void>
}>()

const deleteItem = () => {
  props.onDelete(props.uploadJob.id, props.uploadJob.title);
}
</script>

<template>
  <div class="card">
    <h3 class="card__title">
      <RouterLink :to="`/uploads/${uploadJob.id}`">
        {{ uploadJob.title }}
      </RouterLink>
    </h3>
    <div class="card__body">
      <p>
        <time
          :datetime="new Date(uploadJob.created_at).toISOString()"
          :title="formatDate(uploadJob.created_at, $i18n.locale, true)"
        >
          {{ formatDate(uploadJob.created_at, $i18n.locale) }}
        </time>
      </p>
      <p>
        {{ $t('components.UploadJobCard.file', uploadJob.files_count, { count: uploadJob.files_count }) }}
      </p>
      <div>
        <button
          type="button"
          class="icon-button icon-button--danger"
          @click="deleteItem"
          :title="$t('components.UploadJobsTable.delete')"
          :aria-label="$t('components.UploadJobsTable.delete')"
        >
          <TrashIcon class="icon-button__icon" aria-hidden="true" />
        </button>
      </div>
    </div>
  </div>
</template>
