import { createApp } from 'vue/dist/vue.esm-bundler';
import 'htmx.org'

import UploadQueue from './upload_queue.js'

const uploadQueueApp = createApp(UploadQueue)

uploadQueueApp.mount('#upload-queue')


document.addEventListener('DOMContentLoaded', () => {
  getFormContent();
})

function getFormContent() {
  const el = document.getElementById('upload-job-form');
  el.addEventListener('submit', handleFormSubmit);
}

function handleFormSubmit(event) {
  event.preventDefault();
  const form = event.target;
  const csrfToken = form.elements[0].value;
  const files = [...form.elements[1].files];
  console.log(csrfToken, files);
}
