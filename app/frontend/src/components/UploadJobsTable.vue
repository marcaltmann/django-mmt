<script setup lang="ts">
import type { Header, Item } from 'vue3-easy-data-table'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'

import formatDate from '@/helpers/format-date'
import TrashIcon from '@/icons/TrashIcon.vue'
import type { UploadJob } from '@/types'

const { t } = useI18n()

const props = defineProps<{
  uploadJobs: Array<UploadJob>
  loading: boolean
  onDelete: (uploadJobId: number, title: string) => Promise<void>
}>()

const headers: Header[] = [
  { text: t('components.UploadJobsTable.title'), value: 'title', sortable: true },
  { text: t('components.UploadJobsTable.language'), value: 'language', sortable: true },
  { text: t('components.UploadJobsTable.numFiles'), value: 'files', sortable: true },
  { text: t('components.UploadJobsTable.createdAt'), value: 'created', sortable: true },
  { text: t('components.UploadJobsTable.actions'), value: 'actions' }
]

const items: Item[] = props.uploadJobs.map((uploadJob) => ({
  key: uploadJob.id,
  id: uploadJob.id,
  title: uploadJob.title,
  language: uploadJob.language,
  files: uploadJob.files_count,
  created: new Date(uploadJob.created_at),
  actions: `<button>X</button`
}))

const deleteItem = (val: Item) => {
  props.onDelete(val.id, val.title)
}
</script>

<template>
  <EasyDataTable :headers="headers" :items="items" :loading="loading" alternating>
    <template #item-title="item">
      <RouterLink :to="`/uploads/${item.id}`">
        {{ item.title }}
      </RouterLink>
    </template>
    <template #item-created="item">
      <time
        :datetime="item.created.toISOString()"
        :title="formatDate(item.created, $i18n.locale, true)"
      >
        {{ formatDate(item.created, $i18n.locale) }}
      </time>
    </template>
    <template #item-actions="item">
      <div>
        <button
          type="button"
          class="icon-button icon-button--danger"
          @click="deleteItem(item)"
          :title="$t('components.UploadJobsTable.delete')"
          :aria-label="$t('components.UploadJobsTable.delete')"
        >
          <TrashIcon class="icon-button__icon" aria-hidden="true" />
        </button>
      </div>
    </template>
  </EasyDataTable>
</template>
