<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6 text-center">Данные таблицы</h1>

    <!-- Меню выбора отчетов -->
    <div class="flex justify-center gap-6 mb-6">
      <div class="flex items-center gap-2">
        <label for="start-date" class="text-sm">Начальная дата:</label>
        <input
          type="date"
          id="start-date"
          v-model="startDate"
          class="px-4 py-2 border rounded-md"
        />
      </div>

      <div class="flex items-center gap-2">
        <label for="end-date" class="text-sm">Конечная дата:</label>
        <input
          type="date"
          id="end-date"
          v-model="endDate"
          class="px-4 py-2 border rounded-md"
        />
      </div>

      <button
        @click="fetchData"
        class="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 transition duration-200"
      >
        Загрузить данные
      </button>
      <button
        v-if="userRole === 'admin' || userRole === 'начальник ЦДНГ'"
        @click="saveAsPDF"
        class="bg-red-500 text-white px-6 py-2 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 transition duration-200"
      >
        Сохранить в PDF
      </button>
      <button
        @click="createReport"
        class="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
      >
        Создать отчет
      </button>
    </div>

    <div
      v-if="tableData.length"
      ref="pdfContent"
      class="table-section overflow-x-auto rounded-lg shadow-md border border-gray-300"
    >
      <table
        class="min-w-full bg-white table-auto border-separate border-spacing-0"
      >
        <thead class="bg-blue-600 text-white sticky top-0">
          <tr>
            <th
              v-for="col in columns"
              :key="col"
              class="px-6 py-3 border-b text-left text-sm font-medium"
            >
              {{ getDisplayName(col) }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, index) in tableData"
            :key="index"
            class="even:bg-gray-50 hover:bg-gray-100 transition duration-150"
          >
            <td
              v-for="col in columns"
              :key="col"
              class="px-6 py-3 border-b text-sm text-center"
            >
              {{ formatValue(col, row[col]) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-center text-gray-500 mt-4">
      Данные ещё не загружены.
    </div>
  </div>
</template>

<script>
import axios from "axios";
import html2pdf from "html2pdf.js";
import { jwtDecode } from "jwt-decode";

export default {
  data() {
    return {
      tableData: [],
      columns: [],
      userRole: "",
      startDate: "", // Для начальной даты
      endDate: "", // Для конечной даты
      fieldNameMapping: {
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
      },
    };
  },
  methods: {
    getDisplayName(column) {
      return this.fieldNameMapping[column] || column;
    },
    formatValue(column, value) {
      if (column === "measurement_date" && value) {
        const date = new Date(value);
        return date.toLocaleDateString("ru-RU");
      }
      return value;
    },
    fetchData() {
      const credentials = JSON.parse(localStorage.getItem("db_credentials"));
      const token = localStorage.getItem("access_token");
      if (credentials && token) {
        const decodedToken = jwtDecode(token); // Декодируем JWT для получения информации о пользователе
        this.userRole = decodedToken.role; // Извлекаем роль из токена

        // Параметры с датами
        const params = {
          ...credentials,
          startDate: this.startDate,
          endDate: this.endDate,
        };

        axios
          .get("http://localhost:5000/api/reports", {
            params,
            headers: {
              Authorization: `Bearer ${token}`, // Добавляем токен здесь
            },
          })
          .then((response) => {
            this.tableData = response.data.rows;
            this.columns = response.data.columns;

            localStorage.setItem(
              "report_columns",
              JSON.stringify(this.columns)
            );
            localStorage.setItem("report_data", JSON.stringify(this.tableData));
          })
          .catch((error) => {
            console.error("Ошибка при загрузке данных: ", error);
          });
      } else {
        console.error("Данные подключения не найдены.");
      }
    },
    createReport() {
      this.$router.push({ name: "ReportBuilder" });
    },
    saveAsPDF() {
      // Проверяем роль перед сохранением в PDF
      if (this.userRole === "admin" || this.userRole === "начальник ЦДНГ") {
        const element = this.$refs.pdfContent;

        // Временно отключим scroll и ограничение высоты
        const originalStyle = element.getAttribute("style");
        element.style.maxHeight = "none";
        element.style.overflow = "visible";

        html2pdf()
          .set({
            margin: 10,
            filename: "report.pdf",
            image: { type: "jpeg", quality: 0.98 },
            html2canvas: { scale: 2, scrollY: 0 }, // Отключаем скролл
            jsPDF: { unit: "mm", format: "a4", orientation: "landscape" }, // Лучше использовать ландшафтный формат
          })
          .from(element)
          .save()
          .then(() => {
            if (originalStyle) {
              element.setAttribute("style", originalStyle);
            } else {
              element.removeAttribute("style");
            }
          });
      } else {
        this.errorMessage = "У вас нет прав для сохранения в PDF.";
      }
    },
  },
  mounted() {
    try {
      this.userRole = localStorage.getItem("user_role") || "";
      const storedColumnsRaw = localStorage.getItem("report_columns");
      const storedDataRaw = localStorage.getItem("report_data");

      const storedColumns = storedColumnsRaw
        ? JSON.parse(storedColumnsRaw)
        : null;
      const storedData = storedDataRaw ? JSON.parse(storedDataRaw) : null;

      if (storedColumns && storedData) {
        this.columns = storedColumns;
        this.tableData = storedData;
      } else {
        console.log("Данных в localStorage нет, загрузка через API.");
      }
    } catch (e) {
      console.error("Ошибка чтения из localStorage: ", e);
    }
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th,
td {
  border: 1px solid #000000;
  text-align: center;
  padding: 2px;
}

th {
  background-color: #362841;
  color: white;
  font-weight: 600;
}

td {
  border-bottom: 1px solid #000000;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}

button {
  cursor: pointer;
  font-size: 1rem;
  padding: 10px 5px;
  border-radius: 6px;
  transition: transform 0.2s ease;
}

button:hover {
  transform: scale(1.05);
}

button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.5);
}
</style>
