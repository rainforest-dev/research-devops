import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import pages from "vite-plugin-pages";
import * as path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src/"),
    },
  },
  server: { port: 4000 },
  plugins: [vue(), pages()],
});
