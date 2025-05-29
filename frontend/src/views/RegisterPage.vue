<template>
  <div class="register-page">
    <div class="register-container">
      <h1 class="register-title">Регистрация</h1>

      <form @submit.prevent="registerUser" class="register-form">
        <div class="input-group">
          <label for="username">Имя пользователя (например, Иванов_ИИ):</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            required
            pattern="[А-Яа-яЁёA-Za-z_]{3,}"
            placeholder="Введите имя пользователя"
          />
        </div>

        <div class="input-group">
          <label for="password">Пароль:</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            required
            placeholder="Введите пароль"
          />
        </div>

        <div class="input-group">
          <label for="role">Роль:</label>
          <select v-model="form.role" required>
            <option value="admin">Администратор</option>
            <option value="начальник_ЦДНГ">Начальник ЦДНГ</option>
            <option value="технолог">Технолог</option>
            <option value="механик">Механик</option>
            <option value="энергетик">Энергетик</option>
            <option value="гость">Гость</option>
          </select>
        </div>

        <button type="submit" class="submit-btn">Зарегистрироваться</button>
      </form>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <button class="login-btn" @click="goToLogin">Назад ко входу</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
        role: "",
      },
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await fetch("http://localhost:5000/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.form),
        });
        const data = await response.json();

        if (response.ok) {
          this.successMessage = "Пользователь успешно зарегистрирован!";
          this.errorMessage = "";
        } else {
          this.successMessage = "";
          this.errorMessage = data.message || "Ошибка регистрации.";
        }
      } catch (error) {
        console.error(error);
        this.errorMessage = "Ошибка при подключении к серверу.";
      }
    },
    goToLogin() {
      this.$router.push({ name: "login" });
    },
  },
};
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #eef3f7;
}

.register-container {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  text-align: center;
}

.register-title {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

.register-form {
  display: flex;
  flex-direction: column;
}

.input-group {
  margin-bottom: 15px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

.submit-btn {
  padding: 12px;
  font-size: 1.1rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #218838;
}

.login-btn {
  margin-top: 15px;
  background-color: #6c757d;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.login-btn:hover {
  background-color: #5a6268;
}

.error-message {
  color: #d9534f;
  margin-top: 10px;
}

.success-message {
  color: #28a745;
  margin-top: 10px;
}
</style>
