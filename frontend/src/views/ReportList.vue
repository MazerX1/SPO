<template>
  <div class="container">
    <header>
      <h1>Список отчетов</h1>
    </header>
    <table>
      <thead>
        <tr>
          <th>Название</th>
          <th>Дата</th>
          <th>Роль</th>
          <th>Тип отчета</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="report in reports" :key="report.id">
          <td>{{ report.name }}</td>
          <td>{{ report.report_date }}</td>
          <td>{{ report.user_role }}</td>
          <td>{{ report.report_type }}</td>
          <td>
            <router-link :to="`/reports/edit/${report.id}`" class="btn-edit">
              Редактировать
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
    <router-link to="/reports/create" class="btn-create">
      Создать новый отчет
    </router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      reports: [],
    };
  },
  async created() {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/reports");
      this.reports = await response.json();
    } catch (error) {
      console.error("Ошибка загрузки отчетов: ", error);
    }
  },
};
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

header {
  background: #4caf50;
  color: white;
  padding: 10px;
  text-align: center;
  border-radius: 8px 8px 0 0;
}

h1 {
  margin: 0;
  font-size: 24px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

table th {
  background: #f4f4f4;
}

table tr:nth-child(even) {
  background: #f9f9f9;
}

.btn-edit,
.btn-create {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 12px;
  text-decoration: none;
  color: white;
  border-radius: 4px;
  font-size: 14px;
}

.btn-edit {
  background: #ff9800;
}

.btn-create {
  background: #4caf50;
  display: block;
  text-align: center;
  margin-top: 20px;
}
</style>
