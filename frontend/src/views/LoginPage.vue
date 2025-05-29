<template>
  <div class="login-page">
    <div class="login-container">
      <h1 class="login-title">Вход в систему</h1>

      <form @submit.prevent="loginUser" class="login-form">
        <div class="input-group">
          <label for="username">Пользователь:</label>
          <input
            type="text"
            id="username"
            v-model="credentials.username"
            required
            placeholder="Введите имя пользователя"
          />
        </div>
        <div class="input-group">
          <label for="password">Пароль:</label>
          <input
            type="password"
            id="password"
            v-model="credentials.password"
            required
            placeholder="Введите пароль"
          />
        </div>
        <button type="submit" class="submit-btn">Войти</button>
      </form>

      <button class="register-btn" @click="goToRegister">
        Зарегистрироваться
      </button>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      credentials: {
        username: "",
        password: "",
      },
      errorMessage: "",
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await fetch("http://localhost:5000/api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.credentials),
        });
        const data = await response.json();

        if (response.ok) {
          localStorage.setItem("user_role", data.role);
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("username", this.credentials.username);
          this.$router.push({ name: "home" }); // Перенаправляем на главную страницу
        } else {
          this.errorMessage = data.message;
        }
      } catch (error) {
        console.error(error);
        this.errorMessage = "Ошибка при подключении к серверу.";
      }
    },
    goToRegister() {
      this.$router.push({ name: "register" }); // предполагается, что маршрут регистрации называется 'register'
    },
  },
};
</script>

<style scoped>
/* Остальной стиль без изменений */

.register-btn {
  margin-top: 15px;
  padding: 10px;
  font-size: 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-btn:hover {
  background-color: #5a6268;
}
</style>
