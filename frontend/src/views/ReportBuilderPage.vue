<template>
  <div class="report-builder">
    <h1>Создание отчета</h1>

    <div class="settings">
      <div class="left-column">
        <div>
          <label>Доступные столбцы:</label>
          <select v-model="selectedColumns" size="5" multiple>
            <option v-for="col in columns" :key="col" :value="col">
              {{ col }}
            </option>
          </select>
        </div>

        <div class="buttons">
          <button @click="moveToTable" class="btn">Добавить в таблицу</button>
          <button @click="moveToChart" class="btn">Добавить в график</button>
        </div>
      </div>

      <div class="right-column">
        <div>
          <label>Столбцы для таблицы:</label>
          <ul>
            <li v-for="col in selectedTableColumns" :key="col">{{ col }}</li>
          </ul>
        </div>

        <div>
          <label>Столбцы для графика:</label>
          <ul>
            <li v-for="col in selectedChartColumns" :key="col">{{ col }}</li>
          </ul>
        </div>
      </div>
    </div>

    <button @click="finishReportCreation" class="btn btn-primary">
      Завершить создание отчета
    </button>
  </div>
</template>

<script>
export default {
  name: "ReportBuilderPage",
  data() {
    return {
      columns: [],
      selectedColumns: [],
      selectedTableColumns: [],
      selectedChartColumns: [],
    };
  },
  created() {
    const data = JSON.parse(localStorage.getItem("tableData"));
    if (data && Array.isArray(data.columns)) {
      this.columns = data.columns;
    }
  },
  methods: {
    moveToTable() {
      this.selectedColumns.forEach((col) => {
        if (!this.selectedTableColumns.includes(col)) {
          this.selectedTableColumns.push(col);
        }
      });
    },
    moveToChart() {
      this.selectedColumns.forEach((col) => {
        if (!this.selectedChartColumns.includes(col)) {
          this.selectedChartColumns.push(col);
        }
      });
    },
    finishReportCreation() {
      const reportData = {
        tableColumns: this.selectedTableColumns,
        chartColumns: this.selectedChartColumns,
      };
      localStorage.setItem("reportData", JSON.stringify(reportData));
      this.$router.push({ name: "ReportPage" });
    },
  },
};
</script>

<style scoped>
.report-builder {
  text-align: center;
  margin: 50px auto;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 2rem;
  margin-bottom: 30px;
}

.settings {
  display: flex;
  justify-content: center;
  gap: 50px;
  margin-bottom: 30px;
}

.left-column,
.right-column {
  width: 300px;
}

select {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
}

.buttons {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn {
  background-color: #28a745;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #218838;
}

.btn-primary {
  background-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
