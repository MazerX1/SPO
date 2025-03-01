<template>
  <div id="app">
    <nav>
      <div class="container">
        <router-link to="/" class="logo"> 📊 Отчеты </router-link>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
/* Глобальные стили */
body {
  font-family: "Arial", sans-serif;
  background-color: #f4f4f9;
  margin: 0;
  padding: 0;
  color: #333;
}

/* Навигация */
nav {
  background: #007bff;
  padding: 15px 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
}

.logo:hover {
  opacity: 0.8;
}

/* Основной контент */
main {
  padding: 20px;
  max-width: 1200px;
  margin: 20px auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
</style>
