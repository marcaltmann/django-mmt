import CloseIcon from '../close_icon.js';
import formatBytes from '../format_bytes.js'

export default {
  components: {
    CloseIcon
  },
  props: ['upload'],
  computed: {
    sizeStr() {
      return formatBytes(this.upload.filesize, this.$i18n.locale);
    },
  },
  template: `
    <li class="queue-item">
      <div class="queue-item__body">
        <h3 class="queue-item__name">{{ upload.filename }}</h3>
        <p class="queue-item__details">{{ sizeStr }}</p>
      </div>
      <div class="queue-item__actions">
        <button
          type="button"
          class="queue-item__button icon-button"
          :aria-label="$t('components.UploadQueue.cancel')"
          :title="$t('components.UploadQueue.cancel')"
          @click="$emit('onCancel', upload)"
        >
          <CloseIcon class="queue-item__icon icon-button__icon" />
        </button>
      </div>
    </li>
  `
}
