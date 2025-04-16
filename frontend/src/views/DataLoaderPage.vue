<template>
  <div class="loader-page">
    <h1>Загрузить данные из базы</h1>
    <button @click="loadTables" class="btn">Загрузить таблицы</button>

    <!-- Проверка на наличие таблиц перед их рендерингом -->
    <div v-if="tables && tables.length">
      <h2>Таблицы в базе:</h2>
      <ul>
        <li v-for="table in tables" :key="table">
          {{ table }}
          <button class="btn small" @click="loadTableData(table)">
            Показать данные
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "DataLoaderPage",
  data() {
    return {
      tables: [],
    };
  },
  methods: {
    async loadTables() {
      // Получаем данные подключения из localStorage
      const creds = JSON.parse(localStorage.getItem("db_credentials"));

      if (!creds) {
        this.$router.push({ name: "Home" }); // Если данных нет, возвращаем на главную
        return;
      }

      const response = await fetch("http://localhost:5000/api/load_tables", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(creds),
      });
      const data = await response.json();

      if (data && Array.isArray(data.tables)) {
        this.tables = data.tables;
      } else {
        console.error("Ошибка при загрузке таблиц");
      }
    },

    async loadTableData(tableName) {
      this.selectedTable = tableName;
      const creds = JSON.parse(localStorage.getItem("db_credentials"));

      // Добавляем логирование данных, перед отправкой на сервер
      console.log("Отправляем данные на сервер:", creds);

      const response = await fetch(
        "http://localhost:5000/api/load_table_data",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            ...creds,
            table: tableName,
          }),
        }
      );

      const data = await response.json();

      if (
        response.ok &&
        data &&
        Array.isArray(data.columns) &&
        Array.isArray(data.rows)
      ) {
        // Сохраняем данные в локальном хранилище или состоянии
        localStorage.setItem("tableData", JSON.stringify(data));
        // Переходим на страницу отчёта
        this.$router.push({ name: "TableData" });
      } else {
        console.error(
          "Ошибка при загрузке данных таблицы",
          data.error || "Неизвестная ошибка"
        );
      }
    },
  },
};
</script>

<style scoped>
.loader-page {
  text-align: center;
  margin-top: 50px;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 2rem;
  margin-bottom: 30px;
  color: #343a40;
}

h2 {
  margin-top: 20px;
  font-size: 1.5rem;
  color: #343a40;
}

ul {
  list-style: none;
  padding: 0;
  max-width: 600px;
  margin: 0 auto;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
  padding: 15px;
  margin: 10px 0;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 1.1rem;
  color: #495057;
}

li button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 1rem;
}

li button:hover {
  background-color: #0056b3;
}

.btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 1.1rem;
  cursor: pointer;
  width: 100%;
  max-width: 300px;
  margin: 20px 0;
}

.btn:hover {
  background-color: #218838;
}

@media (max-width: 768px) {
  .btn {
    width: 100%;
  }

  li {
    flex-direction: column;
    align-items: flex-start;
  }

  li button {
    margin-top: 10px;
    width: 100%;
  }
}
</style>
