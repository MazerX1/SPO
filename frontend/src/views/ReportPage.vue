<template>
  <div class="report-page" ref="reportContent">
    <h1>Просмотр отчета</h1>

    <div class="input-container">
      <label for="threshold">Введите пороговое значение:</label>
      <input
        type="number"
        id="threshold"
        v-model.number="thresholdValue"
        placeholder="Порог"
      />

      <label for="highlightColor">Цвет для порога:</label>
      <input type="color" id="highlightColor" v-model="highlightColor" />
    </div>

    <!-- Графики -->
    <div class="charts">
      <div
        v-for="field in reportData.chartColumns"
        :key="field"
        class="chart-container"
      >
        <h3>{{ field }}</h3>
        <canvas :id="'chart-' + field"></canvas>
      </div>
    </div>

    <!-- Таблица -->
    <table class="report-table">
      <thead>
        <tr>
          <th v-for="col in reportData.tableColumns" :key="col">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, rowIndex) in tableData.rows" :key="rowIndex">
          <td
            v-for="col in reportData.tableColumns"
            :key="col"
            :style="getCellStyle(item[col], rowIndex, col)"
            @click="openColorPicker(rowIndex, col)"
          >
            {{ item[col] }}
            <input
              type="color"
              :ref="(el) => setCellColorPickerRef(el)"
              :data-ref-key="`${rowIndex}-${col}`"
              style="display: none"
              @input="setCustomCellColor($event, rowIndex, col)"
            />
          </td>
        </tr>
      </tbody>
    </table>

    <button class="save-button" @click="saveAsPDF" v-if="!isPdfSaving">
      Сохранить отчет в PDF
    </button>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from "vue";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const reportContent = ref(null);

const reportData = reactive({
  tableColumns: [],
  chartColumns: [],
});

const tableData = reactive({
  columns: [],
  rows: [],
});

const thresholdValue = ref(null);
const highlightColor = ref("#ffcccc");
const isPdfSaving = ref(false);

const highlightedCells = reactive({});
const cellColorPickers = ref({});

onMounted(() => {
  const storedReport = JSON.parse(localStorage.getItem("reportData"));
  const storedTable = JSON.parse(localStorage.getItem("tableData"));

  if (storedReport && storedTable) {
    reportData.tableColumns = storedReport.tableColumns;
    reportData.chartColumns = storedReport.chartColumns;
    tableData.columns = storedTable.columns;
    tableData.rows = storedTable.rows;

    nextTick(() => {
      createCharts();
    });
  }
});

function createCharts() {
  reportData.chartColumns.forEach((field) => {
    const ctx = document.getElementById("chart-" + field);
    if (ctx) {
      new Chart(ctx, {
        type: "line",
        data: {
          labels: tableData.rows.map((_, index) => `Точка ${index + 1}`),
          datasets: [
            {
              label: field,
              data: tableData.rows.map((row) => row[field]),
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 2,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "top",
            },
          },
        },
      });
    }
  });
}

function setCellColorPickerRef(el) {
  if (el) {
    const key = el.dataset.refKey;
    cellColorPickers.value[key] = el;
  }
}

function openColorPicker(row, col) {
  const key = `${row}-${col}`;
  const inputEl = cellColorPickers.value[key];
  if (inputEl) inputEl.click();
}

function setCustomCellColor(event, row, col) {
  const color = event.target.value;
  highlightedCells[`${row}-${col}`] = color;
}

function getCellStyle(value, row, col) {
  const key = `${row}-${col}`;
  if (highlightedCells[key]) {
    return { backgroundColor: highlightedCells[key] };
  }
  if (
    thresholdValue.value !== null &&
    !isNaN(value) &&
    value < thresholdValue.value
  ) {
    return { backgroundColor: highlightColor.value };
  }
  return {};
}

async function saveAsPDF() {
  isPdfSaving.value = true;
  await nextTick();

  const element = reportContent.value;
  const canvas = await html2canvas(element, {
    scale: 2,
    useCORS: true,
  });
  const imgData = canvas.toDataURL("image/png");
  const pdf = new jsPDF("p", "mm", "a4");

  const pdfWidth = pdf.internal.pageSize.getWidth();
  const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

  pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);

  const totalPages = pdf.internal.pages.length;
  for (let i = 1; i <= totalPages; i++) {
    pdf.setPage(i);
    pdf.text(
      `Стр. ${i} из ${totalPages}`,
      pdf.internal.pageSize.getWidth() - 50,
      pdf.internal.pageSize.getHeight() - 10
    );
  }

  pdf.save("report.pdf");
  isPdfSaving.value = false;
}
</script>

<style scoped>
.report-page {
  padding: 20px;
  background: white;
  font-family: Arial, sans-serif;
}

.input-container {
  margin-bottom: 20px;
}

.input-container label {
  margin-right: 10px;
}

.input-container input[type="number"] {
  width: 100px;
  margin-right: 20px;
}

.charts {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.chart-container {
  width: 300px;
  height: 300px;
  background: #f9f9f9;
  padding: 10px;
  border-radius: 8px;
}

.report-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}

.report-table th,
.report-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
  cursor: pointer;
}

.save-button {
  display: block;
  margin: 0 auto;
  padding: 12px 24px;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.save-button:hover {
  background-color: #0056b3;
}

@media print {
  .save-button,
  .input-container {
    display: none;
  }

  .report-page {
    width: 210mm;
    margin: 0 auto;
    padding: 20px;
  }

  .charts {
    display: block;
  }

  .chart-container {
    width: 100%;
    margin-bottom: 20px;
  }

  .report-table {
    width: 100%;
    margin-top: 20px;
  }
}
</style>
