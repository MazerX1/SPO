<template>
  <div class="charts">
    <h2>Графики</h2>

    <div v-if="isLoading">Загрузка данных...</div>

    <div v-else-if="chartData && chartData.labels && chartData.labels.length">
      <div class="chart-container">
        <Bar :chart-data="chartData" :chart-options="chartOptions" />
      </div>
    </div>

    <div v-else>
      <p>Нет данных для отображения</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

// Регистрируем компоненты Chart.js
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

const isLoading = ref(true);
const chartData = ref(null);
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
});

onMounted(async () => {
  try {
    // Загружаем данные с вашего API
    const response = await axios.get("http://127.0.0.1:5000/api/data");

    // Преобразуем данные для графика
    const data = response.data;

    chartData.value = {
      labels: data.map((item) => item.name), // Используем поле "name" как метки
      datasets: [
        {
          label: "Средний дебит скважины",
          data: data.map((item) => item.avg_well_debit),
          backgroundColor: "rgba(54, 162, 235, 0.5)",
        },
        {
          label: "Простои (часы)",
          data: data.map((item) => item.downtime_hours),
          backgroundColor: "rgba(255, 99, 132, 0.5)",
        },
        {
          label: "Стоимость электроэнергии",
          data: data.map((item) => item.electricity_cost),
          backgroundColor: "rgba(75, 192, 192, 0.5)",
        },
        {
          label: "Отказ оборудования",
          data: data.map((item) => item.equipment_failures),
          backgroundColor: "rgba(153, 102, 255, 0.5)",
        },
        {
          label: "Газопроизводство",
          data: data.map((item) => item.gas_production),
          backgroundColor: "rgba(255, 159, 64, 0.5)",
        },
        {
          label: "Нефтепроизводство",
          data: data.map((item) => item.oil_production),
          backgroundColor: "rgba(255, 99, 132, 0.5)",
        },
      ],
    };
  } catch (error) {
    console.error("Ошибка при загрузке данных:", error);
  } finally {
    isLoading.value = false; // Снимаем флаг загрузки
  }
});
</script>

<style scoped>
.charts {
  text-align: center;
  padding: 20px;
}

.chart-container {
  width: 80%;
  height: 400px;
  margin: auto;
}
</style>
