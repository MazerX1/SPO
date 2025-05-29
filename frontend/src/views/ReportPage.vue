<template>
  <div class="report-page" ref="reportContent">
    <h1>{{ selectedFormLabel }}</h1>
    <p class="username">Пользователь: {{ username }}</p>

    <div v-if="dataLoaded">
      <table class="report-table">
        <thead>
          <tr>
            <th
              v-for="col in reportData.tableColumns"
              :key="col"
              @click="selectThresholdColumn(col)"
              style="cursor: pointer"
            >
              {{ translateColumn(col) }}
            </th>
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
                :ref="setCellColorPickerRef"
                :data-key="`${rowIndex}-${col}`"
                style="display: none"
                @input="setCustomCellColor($event, rowIndex, col)"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <div class="charts">
        <div
          v-for="field in reportData.chartColumns"
          :key="field"
          class="chart-container"
        >
          <h3>{{ translateColumn(field) }}</h3>
          <canvas :id="'chart-' + field" class="chart-canvas"></canvas>
        </div>
      </div>

      <div class="action-buttons">
        <button class="save-button" @click="saveAsPDF" :disabled="isPdfSaving">
          {{ isPdfSaving ? "Сохраняю..." : "Сохранить отчет в PDF" }}
        </button>
        <button
          class="print-button"
          @click="printReport"
          :style="{ display: isPdfSaving ? 'none' : 'block' }"
        >
          Печать отчета
        </button>
        <button
          class="save-button"
          @click="saveReportToDatabase"
          :style="{ display: isPdfSaving ? 'none' : 'block' }"
        >
          Сохранить отчет в БД
        </button>
      </div>
    </div>

    <div v-else>
      <p>
        Нет данных для отображения отчета. Пожалуйста, вернитесь на предыдущую
        страницу.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from "vue";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

// Основные состояния
const reportContent = ref(null);
const dataLoaded = ref(false);
const isPdfSaving = ref(false);
const highlightColor = ref("#ffcccc");
const username = ref(localStorage.getItem("username") || "");

// Данные отчета
const reportData = reactive({
  tableColumns: [],
  chartColumns: [],
});
const tableData = reactive({ rows: [] });
const selectedFormLabel = ref("");
const anomalyRules = ref([]);
const highlightedCells = reactive({});
const cellColorPickers = ref({});

function selectThresholdColumn(col) {
  const threshold = prompt(
    `Введите пороговое значение для поля "${translateColumn(col)}":`
  );
  if (threshold === null || isNaN(threshold)) {
    alert("Некорректное значение порога.");
    return;
  }

  const color = prompt(
    `Выберите цвет выделения для значений ниже ${threshold} (например: red или #ff0000):`
  );
  if (!color) {
    alert("Цвет не задан.");
    return;
  }

  // Обновим или добавим правило
  const existingIndex = anomalyRules.value.findIndex(
    (r) => r.column_name === col
  );
  if (existingIndex !== -1) {
    anomalyRules.value[existingIndex] = {
      column_name: col,
      threshold_value: Number(threshold),
      color: color,
    };
  } else {
    anomalyRules.value.push({
      column_name: col,
      threshold_value: Number(threshold),
      color: color,
    });
  }

  alert(
    `Правило для "${translateColumn(
      col
    )}" установлено: < ${threshold}, цвет: ${color}`
  );
}

// Загрузка при монтировании
onMounted(async () => {
  const storedReport = JSON.parse(localStorage.getItem("reportData"));
  const storedTable = JSON.parse(localStorage.getItem("report_data"));
  const formOptions = [
    { value: "4", label: "Журнал учета дебитов скважины" },
    { value: "10", label: "Журнал учета ремонтов скважин" },
    { value: "13", label: "Отчет по динамике добычи" },
  ];

  if (storedReport && storedTable) {
    reportData.tableColumns = storedReport.tableColumns || [];
    reportData.chartColumns = storedReport.chartColumns || [];
    tableData.rows = storedTable || [];

    const selectedForm = storedReport.form;
    const form = formOptions.find((f) => f.value === selectedForm);
    selectedFormLabel.value = form ? form.label : "";

    await loadAnomalyRules(selectedForm);

    dataLoaded.value = true;
    await nextTick();
    createCharts();
  }
});

async function loadAnomalyRules(formType) {
  const token = localStorage.getItem("access_token");
  try {
    const response = await fetch(
      `http://localhost:5000/api/anomaly_rules/${formType}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    const data = await response.json();
    anomalyRules.value = data;
  } catch (error) {
    console.error("Ошибка загрузки правил аномалий:", error);
  }
}

function createCharts() {
  reportData.chartColumns.forEach((field) => {
    const ctx = document.getElementById("chart-" + field);
    if (ctx) {
      new Chart(ctx, {
        type: "line",
        data: {
          labels: tableData.rows.map((_, i) => `Точка ${i + 1}`),
          datasets: [
            {
              label: translateColumn(field),
              data: tableData.rows.map((row) => row[field]),
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 2,
              fill: false,
              lineTension: 0,
              pointRadius: 5,
              pointBackgroundColor: "rgba(75, 192, 192, 1)",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: "top" } },
          scales: { x: { beginAtZero: true }, y: { beginAtZero: true } },
        },
      });
    }
  });
}

function setCellColorPickerRef(el) {
  if (el) {
    const key = el.dataset.key;
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
  const rule = anomalyRules.value.find((r) => r.column_name === col);
  if (rule && !isNaN(value) && Number(value) < rule.threshold_value) {
    return { backgroundColor: rule.color || highlightColor.value };
  }
  return {};
}

const fieldNameMapping = {
  id: "№",
  month: "Месяц",
  measurement_date: "Дата измерения",
  liquid_flow: "Дебит жидкости (м³/сут)",
  oil_flow: "Дебит нефти (т/сут)",
  water_cut: "Обводненность (%)",
  notes: "Примечания",
  mode: "Режим",
  pressure: "Давление (атм)",
  exploitation_coefficient: "Коэффициент эксплуатации",
  start_date: "Дата начала",
  end_date: "Дата окончания",
  repair_type: "Тип ремонта",
  repair_reason: "Причина ремонта",
  work_done: "Выполненные работы",
  team: "Бригада",
  result: "Результат",
  well_number: "Номер скважины",
  downtime: "Простой (часы)",
  costs: "Затраты (руб.)",
  period: "Период",
  cumulative_oil: "Кумулятивный дебит нефти (т)",
  deviation: "Отклонение (%)",
};

function translateColumn(col) {
  return fieldNameMapping[col] || col;
}

async function saveAsPDF() {
  isPdfSaving.value = true;
  await nextTick();

  const saveButton = document.querySelector(".save-button");
  const printButton = document.querySelector(".print-button");
  if (saveButton) saveButton.style.display = "none";
  if (printButton) printButton.style.display = "none";

  const element = reportContent.value;
  const canvas = await html2canvas(element, { scale: 2, useCORS: true });
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
      pdfWidth - 50,
      pdf.internal.pageSize.getHeight() - 10
    );
  }

  pdf.save("report.pdf");

  if (saveButton) saveButton.style.display = "block";
  if (printButton) printButton.style.display = "block";

  isPdfSaving.value = false;
}

function printReport() {
  // Создаем скрытый контейнер, который будет содержать только элементы для печати
  const printWindow = window.open("", "_blank", "width=800,height=600");
  printWindow.document.write("<html><head><title>Печать отчета</title>");

  // Добавляем стили для печати
  printWindow.document.write(`
    <style>
      body {
        font-family: Arial, sans-serif;
      }
      .report-page {
        padding: 20px;
        background: white;
      }
      .charts {
        display: block;
        margin-bottom: 30px;
      }
      .chart-container {
        width: 100%;
        margin-bottom: 20px;
      }
      .report-table {
        width: 100%;
        border-collapse: collapse;
      }
      .report-table th,
      .report-table td {
        border: 1px solid #ccc;
        padding: 8px;
        text-align: center;
      }
      .save-button,
      .print-button {
        display: none;
      }
    </style>
  `);

  printWindow.document.write("</head><body>");

  // Копируем содержимое текущей страницы, включая графики
  const reportContent = document.querySelector(".report-page");
  printWindow.document.write(reportContent.innerHTML);

  printWindow.document.write("</body></html>");
  printWindow.document.close();

  // Печатаем содержимое в новом окне
  printWindow.print();
}

const saveReportToDatabase = async () => {
  const token = localStorage.getItem("access_token");
  try {
    const response = await fetch("http://localhost:5000/api/save_report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        form_type: "form4",
        report_data: tableData.rows,
      }),
    });
    const result = await response.json();
    alert(result.message || result.error);
  } catch (error) {
    alert("Ошибка при сохранении отчета: " + error.message);
  }
};
</script>

<style scoped>
.report-page {
  padding: 20px;
  background: white;
  font-family: Arial, sans-serif;
}

.username {
  font-size: 14px;
  margin-bottom: 20px;
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

.chart-canvas {
  width: 100% !important;
  height: 100% !important;
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

.save-button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

@media print {
  .save-button,
  .print-button {
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
