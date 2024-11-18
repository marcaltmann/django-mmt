import { createApp } from 'vue/dist/vue.esm-bundler';
import 'htmx.org'

import UploadQueue from './upload_queue.js'

const uploadQueueApp = createApp(UploadQueue)

uploadQueueApp.mount('#upload-queue')
