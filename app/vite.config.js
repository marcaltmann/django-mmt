import { djangoVitePlugin } from "django-vite-plugin";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    djangoVitePlugin([
      "assets/js/main.js",
      "assets/js/index.js",
      "assets/css/main.css",
    ]),
  ],
});
