from backend.extensions import db

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)  # Идентификатор отчета
    name = db.Column(db.String(255), nullable=False)  # Название отчета
    report_date = db.Column(db.Date, nullable=False)  # Дата отчета
    user_role = db.Column(db.String(100), nullable=False)  # Роль пользователя, создавшего отчет
    oil_production = db.Column(db.Float, nullable=False)  # Добыча нефти
    gas_production = db.Column(db.Float, nullable=False)  # Добыча газа
    avg_well_debit = db.Column(db.Float, nullable=False)  # Среднесуточный дебит
    equipment_failures = db.Column(db.Integer, nullable=False)  # Количество поломок
    downtime_hours = db.Column(db.Float, nullable=False)  # Время простоя
    electricity_cost = db.Column(db.Float, nullable=False)  # Затраты на электроэнергию
    total_cost = db.Column(db.Float, nullable=False)  # Общие затраты

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "report_date": self.report_date,
            "user_role": self.user_role,
            "oil_production": self.oil_production,
            "gas_production": self.gas_production,
            "avg_well_debit": self.avg_well_debit,
            "equipment_failures": self.equipment_failures,
            "downtime_hours": self.downtime_hours,
            "electricity_cost": self.electricity_cost,
            "total_cost": self.total_cost
        }
