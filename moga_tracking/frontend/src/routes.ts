import { createRouter, createWebHashHistory } from "vue-router";
import { setupLayouts } from "virtual:generated-layouts";
import routes from "~pages";

export const router = createRouter({
  history: createWebHashHistory(),
  routes: setupLayouts(routes),
});
