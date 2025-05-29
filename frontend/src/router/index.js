import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/HomePage.vue";
import DataLoaderPage from "@/views/DataLoaderPage.vue";
import ReportPage from "@/views/ReportPage.vue";
import ReportBuilderPage from "@/views/ReportBuilderPage.vue";
import LoginPage from "@/views/LoginPage.vue";
import RegisterPage from "@/views/RegisterPage.vue";

const routes = [
  {
    path: "/home",
    name: "home",
    component: HomePage,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterPage,
  },
  {
    path: "/",
    name: "login",
    component: LoginPage,
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
