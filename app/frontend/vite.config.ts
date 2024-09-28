import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const isDevelopment = process.env.NODE_ENV === 'development'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  base: isDevelopment ? '/' : '/static/',
  build: {
    outDir: '../staticfiles',
    emptyOutDir: true,
  }
})
