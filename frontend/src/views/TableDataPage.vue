<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6 text-center">Данные таблицы</h1>

    <table class="min-w-full bg-white border border-gray-300 mb-6">
      <thead>
        <tr>
          <th
            v-for="col in columns"
            :key="col"
            class="bg-blue-600 text-white px-4 py-2 border"
          >
            {{ getDisplayName(col) }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in tableData" :key="row.id" class="text-center">
          <td v-for="col in columns" :key="col" class="px-4 py-2 border">
            {{ formatValue(col, row[col]) }}
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Кнопка для создания отчета -->
    <div class="text-center">
      <button
        @click="createReport"
        class="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition duration-200"
      >
        Создать отчет
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [], // Сюда будут приходить твои данные
      columns: [], // Сюда придут имена столбцов автоматически
      fieldNameMapping: {
        id: "№",
        name: "Наименование",
        report_date: "Дата отчета",
        user_role: "Роль пользователя",
        oil_production: "Добыча нефти (т/сут)",
        gas_production: "Добыча газа (тыс.м³/сут)",
        avg_well_debit: "Средний дебит скважин (т/сут)",
        equipment_failures: "Отказы оборудования (шт.)",
        downtime_hours: "Часы простоя",
        electricity_cost: "Расход электроэнергии (кВт·ч)",
        total_cost: "Итого расходы (тыс. руб.)",
      },
    };
  },
  methods: {
    getDisplayName(column) {
      return this.fieldNameMapping[column] || column;
    },
    formatValue(column, value) {
      if (column === "report_date" && value) {
        const date = new Date(value);
        return date.toLocaleDateString("ru-RU");
      }
      return value;
    },
    fetchData() {
      // Тут подгружаешь данные, например через API
      // Пока вставлю пример:
      this.tableData = [
        {
          id: 1,
          name: "New Report_1",
          report_date: "2025-02-26T00:00:00Z",
          user_role: "Инженер",
          oil_production: 10,
          gas_production: 15,
          avg_well_debit: 5,
          equipment_failures: 2,
          downtime_hours: 5,
          electricity_cost: 100,
          total_cost: 150,
        },
      ];
      this.columns = Object.keys(this.tableData[0]);
    },
    createReport() {
      // Переход на страницу создания отчета
      this.$router.push({ name: "ReportBuilder" });
    },
  },
  mounted() {
    this.fetchData(); // При загрузке страницы сразу грузим данные
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}
table {
  border-collapse: collapse;
}
th,
td {
  text-align: center;
}

button {
  cursor: pointer;
  font-size: 1.2rem;
}

button:hover {
  background-color: #2563eb;
}
</style>
