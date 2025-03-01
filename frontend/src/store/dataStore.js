import { defineStore } from "pinia";
import axios from "axios";

export const useDataStore = defineStore("dataStore", {
  state: () => ({
    data: [],
  }),
  actions: {
    async loadData() {
      try {
        const response = await axios.get("http://localhost:5000/api/reports"); // Укажи актуальный URL
        this.data = response.data;
      } catch (error) {
        console.error("Ошибка загрузки данных:", error);
      }
    },
  },
});
