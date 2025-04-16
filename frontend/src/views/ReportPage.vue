<template>
  <div class="report-page">
    <h1>Отчет</h1>

    <!-- Графики в одном ряду -->
    <div class="charts">
      <div class="chart-container">
        <LineChart :data="chartData" />
      </div>
      <div class="chart-container">
        <BarChart :data="chartData" />
      </div>
      <div class="chart-container">
        <PieChart :data="chartData" />
      </div>
    </div>

    <!-- Ввод для настройки порога и цвета -->
    <div class="color-settings">
      <label for="threshold">Пороговое значение:</label>
      <input
        type="number"
        v-model="threshold"
        placeholder="Введите пороговое значение"
        min="0"
      />
      <label for="color">Цвет для значений ниже порога:</label>
      <input
        type="color"
        v-model="highlightColor"
        placeholder="Выберите цвет"
      />
    </div>

    <!-- Таблица с выбранными данными -->
    <table>
      <thead>
        <tr>
          <th v-for="col in selectedTableColumns" :key="col">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in tableData" :key="index">
          <td
            v-for="col in selectedTableColumns"
            :key="col"
            :style="{
              backgroundColor: getHighlightColor(row[col]),
            }"
          >
            {{ row[col] }}
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Кнопка для сохранения отчета в PDF -->
    <button @click="saveReportToPDF" class="btn">Сохранить в PDF</button>
  </div>
</template>

<script>
// Импортируем графики и jsPDF
import { Line, Bar, Pie } from "vue-chartjs";
import { jsPDF } from "jspdf";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
} from "chart.js";

// Регистрация графиков
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
);

export default {
  name: "ReportPage",
  components: {
    LineChart: Line,
    BarChart: Bar,
    PieChart: Pie,
  },
  data() {
    return {
      tableData: [],
      selectedTableColumns: [],
      chartData: {
        labels: [],
        datasets: [],
      },
      threshold: 50, // Пороговое значение для выделения
      highlightColor: "#ff0000", // Цвет для значений ниже порога
    };
  },
  created() {
    const reportData = JSON.parse(localStorage.getItem("reportData"));
    if (reportData) {
      this.selectedTableColumns = reportData.tableColumns;
      // Загружаем данные таблицы из localStorage
      const data = JSON.parse(localStorage.getItem("tableData"));
      if (data) {
        this.tableData = data.rows;
        this.updateChartData();
      }
    }
  },
  methods: {
    updateChartData() {
      const labels = this.tableData.map(
        (row) => row[this.selectedTableColumns[0]]
      );
      const dataset = {
        label: "Данные для графика",
        data: this.tableData.map((row) => row[this.selectedTableColumns[1]]), // Пример: берем данные из второго столбца для графика
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      };
      this.chartData.labels = labels;
      this.chartData.datasets = [dataset];
    },

    getHighlightColor(value) {
      // Возвращаем цвет, если значение ниже порога
      return value < this.threshold ? this.highlightColor : "transparent";
    },

    saveReportToPDF() {
      const doc = new jsPDF();
      doc.text("Отчет", 20, 20);

      // Пример добавления таблицы в PDF
      let yPosition = 30;
      this.tableData.forEach((row) => {
        let rowText = this.selectedTableColumns
          .map((col) => row[col])
          .join(" | ");
        doc.text(rowText, 20, yPosition);
        yPosition += 10;
      });

      // Сохраняем PDF
      doc.save("report.pdf");
    },
  },
};
</script>

<style scoped>
.report-page {
  text-align: center;
  margin-top: 50px;
}

.charts {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.chart-container {
  width: 30%;
  margin: 0 10px;
}

table {
  margin: 20px auto;
  border-collapse: collapse;
  width: 80%;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px;
}

th {
  background-color: #007bff;
  color: white;
}

.color-settings {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 20px;
}

input[type="number"],
input[type="color"] {
  padding: 8px;
  font-size: 1rem;
  width: 150px;
}

.btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  cursor: pointer;
  margin-top: 20px;
}

.btn:hover {
  background-color: #218838;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .charts {
    flex-direction: column;
  }

  .chart-container {
    width: 100%;
    margin-bottom: 20px;
  }

  .color-settings {
    flex-direction: column;
  }
}
</style>
