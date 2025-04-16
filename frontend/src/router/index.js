import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/HomePage.vue";
import DataLoaderPage from "@/views/DataLoaderPage.vue";
import ReportPage from "@/views/ReportPage.vue";
import TableDataPage from "@/views/TableDataPage.vue";
import ReportBuilderPage from "@/views/ReportBuilderPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage, // Используем новое имя
  },
  {
    path: "/",
    name: "TableData",
    component: TableDataPage,
  },
  {
    path: "/report-builder",
    name: "ReportBuilder",
    component: ReportBuilderPage,
  },
  {
    path: "/report",
    name: "ReportPage",
    component: ReportPage,
  },
  {
    path: "/data-loader",
    name: "DataLoader",
    component: DataLoaderPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
