<template>
  <div id="app">
    <nav>
      <div class="container">
        <router-link to="/" class="logo">
          📊 Система производственной отчетности
        </router-link>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
/* Навигация */
nav {
  background: #382874; /* Основной цвет навигации */
  padding: 10px 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 22px;
  font-weight: bold;
  color: white;
  text-decoration: none;
  transition: opacity 0.3s ease, color 0.3s ease;
}
</style>
