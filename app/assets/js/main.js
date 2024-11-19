import { createApp } from 'vue/dist/vue.esm-bundler';
import { createI18n } from 'vue-i18n';
import 'htmx.org'

import i18n from './i18n.js'
import UploadJobForm from './components/upload_job_form.js';

const uploadJobFormApp = createApp(UploadJobForm);
uploadJobFormApp.use(i18n);

document.addEventListener('DOMContentLoaded', () => {
});
