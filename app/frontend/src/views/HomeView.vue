<script setup lang="ts">
import { RouterLink } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
</script>

<template>
  <main class="container u-mt u-mb-2">
    <h2>
      {{ $t('views.HomeView.title') }}
    </h2>

    <p v-if="store.user?.can_upload" class="u-font-large u-ll u-mt">
      <RouterLink to="/new-upload">
        {{ $t('views.HomeView.newUpload') }}
      </RouterLink>
    </p>

    <p v-if="store.user?.can_upload" class="u-font-large u-ll u-mt">
      <RouterLink to="/uploads">
        {{ $t('views.HomeView.uploads') }}
      </RouterLink>
    </p>

    <p class="u-font-large u-ll u-mt">
      <RouterLink to="/downloads">
        {{ $t('views.HomeView.downloads') }}
      </RouterLink>
    </p>
  </main>
</template>
