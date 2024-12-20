import { addMilliseconds, formatDistance } from "date-fns";
import { de } from "date-fns/locale";

import formatBytes from "../helpers/format_bytes.js";
import remainingTime from "../helpers/remaining_time.js";
import CloseIcon from "./close_icon.js";
import ProgressBar from "./progress_bar.js";

export default {
  components: {
    CloseIcon,
    ProgressBar,
  },
  props: ["upload"],
  computed: {
    sizeStr() {
      return formatBytes(this.upload.filesize, this.$i18n.locale);
    },
    filePercentage() {
      if (!this.upload) {
        return 0;
      }
      return (this.upload.transferred / this.upload.filesize) * 100;
    },
    checksumPercentage() {
      if (!this.upload) {
        return 0;
      }
      return (this.upload.checksumProgress / 1) * 100;
    },
    timeToGo() {
      const localeOptions = {};
      if (this.$i18n.locale === "de") {
        localeOptions.locale = de;
      }

      let remainingMilliseconds;
      const now = new Date();
      let futureDate = new Date();
      if (this.upload?.transferred) {
        remainingMilliseconds = remainingTime(
          this.upload.startedAt,
          this.upload.filesize,
          this.upload.transferred,
        );
        futureDate = addMilliseconds(now, remainingMilliseconds);
      }

      return formatDistance(futureDate, now, {
        ...localeOptions,
      });
    },
  },
  template: `
    <li class="queue-item queue-item--is-active">
      <div class="queue-item__body">
        <h3 class="queue-item__name">
          {{ this.upload?.serverFilename }}
        </h3>
        <p class="queue-item__details">
          {{ sizeStr }} <span>– {{ timeToGo }}</span>
        </p>
        <ProgressBar
          id="upload-progress"
          :percentage="filePercentage"
          color="#bed7ff"
          :label="$t('upload')"
        />
        <ProgressBar
          id="checksum-progress"
          :percentage="checksumPercentage"
          color="#c7ffbe"
          :label="$t('checksum')"
        />
      </div>
      <div class="queue-item__actions">
        <button
          type="button"
          class="queue-item__button icon-button"
          :aria-label="$t('cancel')"
          :title="$t('cancel')"
          @click="$emit('onCancelActive')"
        >
          <CloseIcon class="queue-item__icon icon-button__icon" />
        </button>
      </div>
    </li>
  `,
};
