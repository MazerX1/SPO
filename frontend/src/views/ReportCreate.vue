<template>
  <div class="container">
    <h1>Создать новый отчет</h1>
    <form class="report-form" @submit.prevent="createReport">
      <div class="form-group">
        <label for="name">Название</label>
        <input id="name" type="text" v-model="report.name" required />
      </div>
      <div class="form-group">
        <label for="report_date">Дата</label>
        <input
          id="report_date"
          v-model="report.report_date"
          type="date"
          required
        />
      </div>
      <div class="form-group">
        <label for="user_role">Роль</label>
        <input id="user_role" type="text" v-model="report.user_role" required />
      </div>
      <div class="form-group">
        <label for="oil_production">Добыча нефти</label>
        <input
          id="oil_production"
          v-model="report.oil_production"
          type="number"
          required
        />
      </div>
      <div class="form-group">
        <label for="gas_production">Добыча газа</label>
        <input
          id="gas_production"
          v-model="report.gas_production"
          type="number"
          required
        />
      </div>
      <div class="form-group">
        <label for="avg_well_debit">Средний дебит скважины</label>
        <input
          id="avg_well_debit"
          v-model="report.avg_well_debit"
          type="number"
          required
        />
      </div>
      <div class="form-group">
        <label for="equipment_failures">Неисправности оборудования</label>
        <input
          id="equipment_failures"
          v-model="report.equipment_failures"
          type="number"
          required
        />
      </div>
      <div class="form-group">
        <label for="downtime_hours">Часы простоя</label>
        <input
          id="downtime_hours"
          v-model="report.downtime_hours"
          type="number"
          required
        />
      </div>
      <div class="form-group">
        <label for="electricity_cost">Затраты на электроэнергию</label>
        <input
          id="electricity_cost"
          v-model="report.electricity_cost"
          type="number"
          required
        />
      </div>
      <div class="form-group">
        <label for="total_cost">Общие затраты</label>
        <input
          id="total_cost"
          v-model="report.total_cost"
          type="number"
          required
        />
      </div>
      <div class="form-actions">
        <button type="submit" class="btn">Создать</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      report: {
        name: "",
        report_date: "",
        user_role: "",
        oil_production: "",
        gas_production: "",
        avg_well_debit: "",
        equipment_failures: "",
        downtime_hours: "",
        electricity_cost: "",
        total_cost: "",
      },
    };
  },
  methods: {
    async createReport() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/reports", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.report),
        });
        await response.json();
        this.$router.push("/"); // Редирект на страницу списка отчетов
      } catch (error) {
        console.error("Ошибка при создании отчета:", error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
}

.report-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
  color: #444;
}

input,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

input:focus,
select:focus {
  border-color: #007bff;
  outline: none;
}

.form-actions {
  text-align: center;
}

.btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background-color: #218838;
}
</style>
