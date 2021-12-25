import { createApp } from "vue";
import { router } from "./routes";
import VueApexCharts from "vue3-apexcharts";
import App from "./App.vue";
import "./index.css";

const app = createApp(App);
app.use(router);
app.use(VueApexCharts);
app.mount("#app");
