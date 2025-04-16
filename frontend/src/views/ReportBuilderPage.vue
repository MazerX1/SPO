<template>
  <div class="report-builder">
    <h1>Создание отчета</h1>

    <div class="settings">
      <div class="left-column">
        <div>
          <label for="tableColumns">Выберите столбцы для таблицы:</label>
          <select v-model="selectedTableColumns" size="5" multiple>
            <option v-for="col in columns" :key="col" :value="col">
              {{ col }}
            </option>
          </select>
          <button @click="moveToTable" class="btn">→</button>
        </div>

        <div>
          <label for="chartColumns">Выберите столбцы для графика:</label>
          <select v-model="selectedChartColumns" size="5" multiple>
            <option v-for="col in columns" :key="col" :value="col">
              {{ col }}
            </option>
          </select>
          <button @click="moveToChart" class="btn">→</button>
        </div>
      </div>

      <div class="right-column">
        <div>
          <label for="selectedTableColumns"
            >Выбранные столбцы для таблицы:</label
          >
          <ul>
            <li v-for="col in selectedTableColumns" :key="col">{{ col }}</li>
          </ul>
        </div>

        <div>
          <label for="selectedChartColumns"
            >Выбранные столбцы для графика:</label
          >
          <ul>
            <li v-for="col in selectedChartColumns" :key="col">{{ col }}</li>
          </ul>
        </div>
      </div>
    </div>

    <button @click="finishReportCreation" class="btn">
      Завершить создание отчета
    </button>
  </div>
</template>

<script>
export default {
  name: "ReportBuilderPage",
  data() {
    return {
      columns: [], // Список всех столбцов
      selectedTableColumns: [], // Выбранные столбцы для таблицы
      selectedChartColumns: [], // Выбранные столбцы для графика
    };
  },
  created() {
    // Загружаем данные таблицы из localStorage
    const data = JSON.parse(localStorage.getItem("tableData"));
    if (data && Array.isArray(data.columns)) {
      this.columns = data.columns;
    }
  },
  methods: {
    moveToTable() {
      // Перемещаем выбранный столбец для таблицы в список
      this.selectedTableColumns.push(
        this.columns.find(
          (col) =>
            col ===
            this.selectedTableColumns[this.selectedTableColumns.length - 1]
        )
      );
    },
    moveToChart() {
      // Перемещаем выбранный столбец для графика в список
      this.selectedChartColumns.push(
        this.columns.find(
          (col) =>
            col ===
            this.selectedChartColumns[this.selectedChartColumns.length - 1]
        )
      );
    },
    finishReportCreation() {
      // Сохраняем выбранные настройки отчета
      const reportData = {
        tableColumns: this.selectedTableColumns,
        chartColumns: this.selectedChartColumns,
      };
      localStorage.setItem("reportData", JSON.stringify(reportData));

      // Переходим на страницу отчета
      this.$router.push({ name: "ReportPage" });
    },
  },
};
</script>

<style scoped>
.report-builder {
  text-align: center;
  margin-top: 50px;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 2rem;
  margin-bottom: 30px;
  color: #343a40;
  font-weight: bold;
}

.settings {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.left-column,
.right-column {
  width: 45%;
}

h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #495057;
}

label {
  font-weight: bold;
  color: #495057;
}

select {
  margin-top: 10px;
  padding: 8px;
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  color: #495057;
  background-color: #f9f9f9;
}

select:focus {
  outline: none;
  border-color: #007bff;
}

.btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 12px 24px;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 15px;
}

.btn:hover {
  background-color: #218838;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 5px;
}

@media (max-width: 768px) {
  .settings {
    flex-direction: column;
  }

  .left-column,
  .right-column {
    width: 100%;
    margin-bottom: 20px;
  }

  .btn {
    width: 100%;
  }
}
</style>
