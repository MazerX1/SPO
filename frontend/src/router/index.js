import { createRouter, createWebHistory } from "vue-router";
import Reports from "../views/ReportList.vue";
import ReportCreate from "../views/ReportCreate.vue";
import ReportEdit from "../views/ReportEdit.vue"; // Должен быть импорт

import HomePage from "../views/HomePage.vue";
import ChartsPage from "../views/ChartsPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage, // Используем новое имя
  },
  {
    path: "/reports",
    name: "reports",
    component: Reports,
  },
  {
    path: "/reports/create",
    name: "create-report",
    component: ReportCreate,
  },
  {
    path: "/reports/edit/:id",
    name: "edit-report",
    component: ReportEdit,
  },
  {
    path: "/charts",
    name: "charts",
    component: ChartsPage, // Используем новое имя
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
