<template>
  <div class="table-page">
    <h1>Данные таблицы</h1>

    <!-- Таблица с данными -->
    <table>
      <thead>
        <tr>
          <th v-for="col in columns" :key="col">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in tableData" :key="index">
          <td v-for="col in columns" :key="col">{{ row[col] }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Кнопка для перехода на страницу создания отчета -->
    <button @click="goToReportBuilder" class="btn">Создать отчет</button>
  </div>
</template>

<script>
export default {
  name: "TableDataPage",
  data() {
    return {
      columns: [], // Список столбцов
      tableData: [], // Данные таблицы
    };
  },
  created() {
    // Загружаем данные таблицы из localStorage
    const data = JSON.parse(localStorage.getItem("tableData"));
    if (data && Array.isArray(data.columns) && Array.isArray(data.rows)) {
      this.columns = data.columns;
      this.tableData = data.rows;
    }
  },
  methods: {
    goToReportBuilder() {
      // Переходим к странице создания отчета
      this.$router.push({ name: "ReportBuilder" });
    },
  },
};
</script>

<style scoped>
.table-page {
  text-align: center;
  margin-top: 50px;
  font-family: Arial, sans-serif;
  padding: 0 20px; /* Добавлены отступы для предотвращения залипания к краям на мобильных устройствах */
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #343a40;
  font-weight: bold;
}

table {
  margin: 20px auto;
  border-collapse: collapse;
  width: 100%; /* Убедимся, что таблица будет занимать всю ширину экрана */
  max-width: 1200px;
}

th,
td {
  border: 1px solid #ccc;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

td {
  background-color: #f9f9f9;
  color: #495057;
}

tr:nth-child(even) td {
  background-color: #f1f1f1;
}

tr:hover td {
  background-color: #e9ecef;
}

.btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 12px 20px;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 30px;
  width: 220px;
  max-width: 100%; /* Делаем кнопку адаптивной */
  display: block; /* Кнопка будет занимать всю ширину на мобильных устройствах */
  margin-left: auto;
  margin-right: auto;
}

.btn:hover {
  background-color: #218838;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  table {
    width: 100%; /* Растягиваем таблицу на всю ширину */
  }

  th,
  td {
    padding: 10px; /* Уменьшаем padding на мобильных устройствах */
  }

  .btn {
    width: 100%; /* Кнопка будет занимать всю ширину на мобильных устройствах */
    padding: 14px 0;
  }
}
</style>
