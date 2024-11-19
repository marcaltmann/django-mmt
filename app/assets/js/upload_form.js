import { createApp } from 'vue/dist/vue.esm-bundler';

import i18n from './i18n.js'
import UploadQueueStarter from './components/upload_queue_starter.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('upload-job-form');

  form.addEventListener('submit', event => {
    event.preventDefault();

    const csrfEl = document.querySelectorAll('[name="csrfmiddlewaretoken"]')[0];
    const token = csrfEl.value;

    const fileInput = form.elements[1];
    const files = [...fileInput.files];

    const titleInput = form.elements[2];
    const title = titleInput.value.trim();

    const app = createApp(UploadQueueStarter, {
      title,
      files,
      csrfToken: token,
    });
    app.use(i18n);
    app.mount('#upload-job-form');
  });
});
