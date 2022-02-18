import { createApp } from "vue";
import "reflect-metadata";
import { router } from "./routes";
import VueApexCharts from "vue3-apexcharts";
import VueLazyLoad from "vue3-lazyload";
import App from "./App.vue";
import "./index.css";

const app = createApp(App);
app.use(router);
app.use(VueLazyLoad, {});
app.use(VueApexCharts);
app.mount("#app");
