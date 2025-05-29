from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date

from backend.extensions import db

Base = declarative_base()

class Form4Measurement(db.Model):
    __tablename__ = 'well_flow_journal'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    measurement_date = db.Column(db.Date, nullable=False)
    liquid_flow = db.Column(db.Numeric(10, 2), nullable=False)
    oil_flow = db.Column(db.Numeric(10, 2), nullable=False)
    water_cut = db.Column(db.Numeric(5, 2), nullable=False)
    notes = db.Column(db.Text)
    mode = db.Column(db.String(20))
    pressure = db.Column(db.Numeric(10, 2))
    exploitation_coefficient = db.Column(db.Numeric(5, 2))
    created_by = db.Column(db.String(50), nullable=False)

class Form10Repair(db.Model):
    __tablename__ = 'well_repair_journal'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    repair_type = db.Column(db.String(50), nullable=False)
    repair_reason = db.Column(db.String(255), nullable=False)
    work_done = db.Column(db.Text)
    team = db.Column(db.String(50))
    result = db.Column(db.Text)
    well_number = db.Column(db.Integer)
    downtime = db.Column(db.Integer)
    costs = db.Column(db.Numeric(15, 2))
    created_by = db.Column(db.String(50), nullable=False)

class Form13Dynamics(db.Model):
    __tablename__ = 'production_dynamics_report'

    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(20), nullable=False)
    oil_flow = db.Column(db.Numeric(10, 2), nullable=False)
    liquid_flow = db.Column(db.Numeric(10, 2), nullable=False)
    water_cut = db.Column(db.Numeric(5, 2), nullable=False)
    cumulative_oil = db.Column(db.Numeric(10, 2), nullable=False)
    deviation = db.Column(db.Numeric(5, 2))
    created_by = db.Column(db.String(50), nullable=False)

class FormNew(db.Model):
    __tablename__ = 'form_new'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20))
    measurement_date = db.Column(db.Date)
    liquid_flow = db.Column(db.Numeric(10, 2))
    oil_flow = db.Column(db.Numeric(10, 2))
    water_cut = db.Column(db.Numeric(5, 2))
    notes = db.Column(db.Text)
    mode = db.Column(db.String(50))
    pressure = db.Column(db.Numeric(6, 2))
    exploitation_coefficient = db.Column(db.Numeric(5, 2))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    repair_type = db.Column(db.String(100))
    repair_reason = db.Column(db.String(200))
    work_done = db.Column(db.Text)
    team = db.Column(db.String(100))
    result = db.Column(db.String(100))
    well_number = db.Column(db.String(50))
    downtime = db.Column(db.Numeric(6, 2))
    costs = db.Column(db.Numeric(12, 2))
    period = db.Column(db.String(20))
    cumulative_oil = db.Column(db.Numeric(12, 2))
    deviation = db.Column(db.Numeric(6, 2))
    created_by = db.Column(db.String(50), nullable=False)

class AnomalyRule(db.Model):
    __tablename__ = 'anomaly_rules'
    id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(50), nullable=False)
    column_name = db.Column(db.String(50), nullable=False)
    threshold_value = db.Column(db.Float, nullable=False)
    highlight_color = db.Column(db.String(7), nullable=False)  # Для хранения цвета в формате #RRGGBB