<template>
  <div class="loader-page">
    <h1>Подключение к базе данных</h1>

    <form @submit.prevent="connectToDatabase">
      <!-- Выпадающий список баз -->
      <div>
        <label for="database">Выберите базу данных:</label>
        <select v-model="selectedDatabase" @change="onDatabaseChange" required>
          <option disabled value="">Выберите...</option>
          <option
            v-for="db in standardDatabases"
            :key="db.name"
            :value="db.name"
          >
            {{ db.name }}
          </option>
        </select>
      </div>

      <!-- Поля ручного ввода, если выбрано "Другое" -->
      <div v-if="manualInput">
        <div>
          <label for="username">Пользователь:</label>
          <input
            type="text"
            v-model="dbCredentials.username"
            id="username"
            required
          />
        </div>
        <div>
          <label for="password">Пароль:</label>
          <input
            type="password"
            v-model="dbCredentials.password"
            id="password"
            required
          />
        </div>
        <div>
          <label for="dbname">Имя базы данных:</label>
          <input
            type="text"
            v-model="dbCredentials.dbname"
            id="dbname"
            required
          />
        </div>
      </div>

      <button type="submit">Подключиться</button>
    </form>

    <div v-if="tables.length">
      <h2>Таблицы в базе:</h2>
      <ul>
        <li v-for="table in tables" :key="table">{{ table }}</li>
      </ul>
    </div>

    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dbCredentials: {
        username: "",
        password: "",
        dbname: "",
      },
      tables: [],
      errorMessage: "",

      // Список стандартных баз данных
      standardDatabases: [
        {
          name: "Производственная база",
          dbname: "production_db",
          username: "myuser",
          password: "mypassword",
        },
        {
          name: "Тестовая база",
          dbname: "test_db",
          username: "test_user",
          password: "test_pass",
        },
        { name: "Другое (ввести вручную)", dbname: "" },
      ],
      selectedDatabase: "", // Что выбрал пользователь
      manualInput: false, // Нужно ли вручную вводить данные
    };
  },
  methods: {
    async connectToDatabase() {
      try {
        // Сохраняем данные подключения в localStorage
        localStorage.setItem(
          "db_credentials",
          JSON.stringify(this.dbCredentials)
        );

        // Отправляем запрос на сервер
        const response = await fetch("http://localhost:5000/api/load_tables", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.dbCredentials),
        });
        const data = await response.json();

        if (response.ok) {
          this.tables = data.tables;
          this.errorMessage = "";

          // Перенаправление на страницу загрузки данных
          this.$router.push({ name: "DataLoader" });
        } else {
          this.errorMessage =
            data.error || "Ошибка при подключении к базе данных";
          this.tables = [];
        }
      } catch (error) {
        this.errorMessage = "Ошибка при запросе на сервер";
        console.error(error);
      }
    },

    onDatabaseChange() {
      const selected = this.standardDatabases.find(
        (db) => db.name === this.selectedDatabase
      );

      if (selected && selected.dbname) {
        // Если выбрана стандартная база — заполняем данные
        this.dbCredentials.username = selected.username;
        this.dbCredentials.password = selected.password;
        this.dbCredentials.dbname = selected.dbname;
        this.manualInput = false;
      } else {
        // Если выбрано "Другое" — очищаем и даем вручную вводить
        this.dbCredentials.username = "";
        this.dbCredentials.password = "";
        this.dbCredentials.dbname = "";
        this.manualInput = true;
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
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  margin: 0 auto;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

form div {
  margin-bottom: 15px;
  width: 100%;
}

label {
  display: block;
  font-size: 1rem;
  margin-bottom: 5px;
  color: #495057;
}

input,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus,
select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  width: 100%;
}

button:hover {
  background-color: #218838;
}

.error {
  color: red;
  font-size: 1.2rem;
  margin-top: 20px;
}

h2 {
  margin-top: 30px;
  font-size: 1.5rem;
  color: #333;
}

ul {
  list-style: none;
  padding: 0;
}

ul li {
  background-color: #f1f3f5;
  padding: 10px;
  margin: 5px 0;
  border-radius: 4px;
  font-size: 1rem;
  color: #343a40;
}
</style>
