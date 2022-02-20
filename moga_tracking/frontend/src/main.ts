import { createApp } from "vue";
import "reflect-metadata";
import { router } from "./routes";
import VueLazyLoad from "vue3-lazyload";
import App from "./App.vue";
import "./index.css";

const app = createApp(App);
app.use(router);
app.use(VueLazyLoad, {});
app.mount("#app");
