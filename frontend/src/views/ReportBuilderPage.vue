<template>
  <div class="report-builder">
    <h1>Создание/Редактирование отчета</h1>

    <!-- Выбор формы отчета -->
    <div class="form-selection">
      <label for="form-select">Выберите форму отчета:</label>
      <select v-model="selectedForm" @change="loadFormData" id="form-select">
        <option
          v-for="form in formOptions"
          :key="form.value"
          :value="form.value"
        >
          {{ form.label }}
        </option>
      </select>
    </div>

    <div class="settings">
      <div class="left-column">
        <div>
          <label>Доступные столбцы:</label>
          <select v-model="selectedColumns" size="5" multiple>
            <option v-for="col in columns" :key="col.field" :value="col.field">
              {{ col.label }}
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
            <li v-for="col in selectedTableColumns" :key="col">
              {{ translateColumn(col) }}
              <button @click="removeFromTable(col)">Удалить</button>
            </li>
          </ul>
        </div>

        <div>
          <label>Столбцы для графика:</label>
          <ul>
            <li v-for="col in selectedChartColumns" :key="col">
              {{ translateColumn(col) }}
              <button @click="removeFromChart(col)">Удалить</button>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="buttons">
      <button @click="finishReportCreation" class="btn btn-primary">
        Завершить создание/редактирование отчета
      </button>
      <button @click="saveForm" class="btn btn-secondary">
        Сохранить форму
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReportBuilderPage",
  data() {
    return {
      formOptions: [
        { value: "4", label: "Форма 4 Журнал учета дебитов скважины" },
        { value: "10", label: "Форма 10 Журнал учета ремонтов скважин" },
        { value: "13", label: "Форма 13 Отчет по динамике добычи" },
        { value: "new", label: "Создать новую форму" }, // Опция для создания новой формы
      ],
      columns: [], // [{ field, label }]
      selectedColumns: [], // выбранные в мультиселекте (field)
      selectedTableColumns: [],
      selectedChartColumns: [],
      selectedForm: "4", // По умолчанию выбранная форма
    };
  },
  methods: {
    // Загрузка данных для выбранной формы
    async loadFormData() {
      if (this.selectedForm === "new") {
        // Для новой формы очищаем поля
        this.columns = [
          { field: "month", label: "Месяц" },
          { field: "measurement_date", label: "Дата измерения" },
          { field: "liquid_flow", label: "Дебит жидкости" },
          { field: "oil_flow", label: "Дебит нефти" },
          { field: "water_cut", label: "Обводненность" },
          { field: "notes", label: "Примечания" },
          { field: "mode", label: "Режим работы" },
          { field: "pressure", label: "Давление" },
          {
            field: "exploitation_coefficient",
            label: "Коэффициент эксплуатации",
          },
          { field: "start_date", label: "Дата начала" },
          { field: "end_date", label: "Дата окончания" },
          { field: "repair_type", label: "Тип ремонта" },
          { field: "repair_reason", label: "Причина ремонта" },
          { field: "work_done", label: "Выполненные работы" },
          { field: "team", label: "Команда" },
          { field: "result", label: "Результат" },
          { field: "well_number", label: "Номер скважины" },
          { field: "downtime", label: "Простой" },
          { field: "costs", label: "Затраты" },
          { field: "period", label: "Период" },
          { field: "cumulative_oil", label: "Накопленная нефть" },
          { field: "deviation", label: "Отклонение" },
          { field: "created_by", label: "Создано пользователем" },
        ];
        this.selectedColumns = [];
        this.selectedTableColumns = [];
        this.selectedChartColumns = [];
        return;
      }

      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://localhost:5000/api/form_columns/${this.selectedForm}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );
        const data = await response.json();
        if (data.error) {
          alert("Ошибка: " + data.error);
          return;
        }
        this.columns = data.columns;
        this.selectedColumns = [];
        this.selectedTableColumns = [];
        this.selectedChartColumns = [];
        localStorage.setItem("report_columns", JSON.stringify(this.columns));
      } catch (error) {
        console.error("Ошибка загрузки данных формы:", error);
      }
    },

    // Добавление выбранных столбцов в таблицу
    moveToTable() {
      this.selectedColumns.forEach((col) => {
        if (!this.selectedTableColumns.includes(col)) {
          this.selectedTableColumns.push(col);
        }
      });
    },

    // Добавление выбранных столбцов в график
    moveToChart() {
      this.selectedColumns.forEach((col) => {
        if (!this.selectedChartColumns.includes(col)) {
          this.selectedChartColumns.push(col);
        }
      });
    },

    // Завершение создания отчета
    finishReportCreation() {
      const reportData = {
        form: this.selectedForm,
        tableColumns: this.selectedTableColumns,
        chartColumns: this.selectedChartColumns,
      };

      localStorage.setItem("reportData", JSON.stringify(reportData));
      this.$router.push({ name: "ReportPage" });
    },

    // Перевод названия столбца
    translateColumn(field) {
      const col = this.columns.find((c) => c.field === field);
      return col ? col.label : field;
    },

    // Удалить столбец из таблицы
    removeFromTable(col) {
      this.selectedTableColumns = this.selectedTableColumns.filter(
        (c) => c !== col
      );
    },

    // Удалить столбец из графика
    removeFromChart(col) {
      this.selectedChartColumns = this.selectedChartColumns.filter(
        (c) => c !== col
      );
    },

    // Сохранение формы
    saveForm() {
      const formData = {
        form: this.selectedForm,
        tableColumns: this.selectedTableColumns,
        chartColumns: this.selectedChartColumns,
        data: this.formData, // Данные, введенные для новой формы
      };

      fetch("http://localhost:5000/api/save_form", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(formData),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert("Форма успешно сохранена");
            this.loadFormData(); // Перезагружаем данные после сохранения
          } else {
            alert("Ошибка при сохранении формы");
          }
        })
        .catch((error) => {
          console.error("Ошибка при сохранении формы:", error);
        });
    },
  },
  mounted() {
    this.loadFormData(); // При загрузке страницы загружаем данные по умолчанию
    const storedColumns = JSON.parse(
      localStorage.getItem("report_columns") || "[]"
    );
    const storedData = JSON.parse(localStorage.getItem("report_data") || "[]");

    if (storedColumns.length && storedData.length) {
      this.columns = storedColumns;
      this.tableData = storedData;
    } else {
      console.warn("Нет сохранённых данных для отчёта.");
    }
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

.form-selection {
  margin-bottom: 20px;
}
</style>
