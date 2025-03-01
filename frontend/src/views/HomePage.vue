<template>
  <div class="home">
    <h1>Добро пожаловать в систему отчетности</h1>

    <div v-if="isLoading">Загрузка данных...</div>

    <div v-else-if="data.length">
      <h2>Загруженные данные</h2>
      <table>
        <thead>
          <tr>
            <th>Отчет</th>
            <th>Дата</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="report in data" :key="report.id">
            <td>{{ report.name }}</td>
            <td>{{ formatDate(report.report_date) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else>
      <p>Нет данных для отображения.</p>
    </div>

    <div class="buttons">
      <router-link to="/reports" class="btn"> Перейти к отчетам </router-link>
      <router-link to="/charts" class="btn"> Просмотр графиков </router-link>
    </div>
  </div>
</template>

<script>
import { useDataStore } from "@/store/dataStore";
import { storeToRefs } from "pinia";
import { computed, onMounted } from "vue";

export default {
  name: "HomePage",
  setup() {
    const store = useDataStore();
    const { data } = storeToRefs(store);
    const isLoading = computed(() => data.value.length === 0);

    onMounted(() => {
      store.loadData();
    });

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString("ru-RU");
    };

    return {
      data,
      isLoading,
      formatDate,
    };
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}

table {
  width: 50%;
  margin: 20px auto;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ccc;
  padding: 10px;
}

th {
  background-color: #007bff;
  color: white;
}

td {
  text-align: center;
}

.buttons {
  margin-top: 20px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  margin: 10px;
  font-size: 18px;
  color: white;
  background-color: #007bff;
  border-radius: 5px;
  text-decoration: none;
  cursor: pointer;
  border: none;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
