from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from datetime import datetime

from backend.models.models import Form4Measurement, Form10Repair, Form13Dynamics, FormNew, AnomalyRule
# Создание Blueprint для работы с отчетами
report_bp = Blueprint('report_bp', __name__)

# Преобразование строки даты
def parse_date(value):
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S GMT").date()
        except ValueError:
            return None
    return value  # если уже date или None
# Сохранение отчета
@report_bp.route('/api/save_report', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)
def save_report():
    # Обработка CORS preflight запроса
    if request.method == 'OPTIONS':
        return '', 200  # Ответ для CORS preflight

    try:
        data = request.get_json()
        form_type = data.get("form_type")
        report_data = data.get("report_data")
        # Проверка наличия обязательных полей
        if not form_type or not report_data:
            return jsonify({"error": "Неверный формат запроса"}), 400

        # Сопоставление форм с моделями
        model_map = {
            "form4": Form4Measurement,
            "form10": Form10Repair,
            "form13": Form13Dynamics,
            "form_new": FormNew,
        }
        # Допустимые модели для каждой формы
        form_fields = {
            "form4": {
                "month", "measurement_date", "liquid_flow", "oil_flow",
                "water_cut", "notes", "mode", "pressure", "exploitation_coefficient"
            },
            "form10": {
                "start_date", "end_date", "repair_type", "repair_reason",
                "work_done", "team", "result", "well_number", "downtime", "costs"
            },
            "form13": {
                "period", "oil_flow", "liquid_flow", "water_cut", "cumulative_oil", "deviation"
            },
            "form_new": {
                "month", "measurement_date", "liquid_flow", "oil_flow", "water_cut", "notes",
                "mode", "pressure", "exploitation_coefficient", "start_date", "end_date",
                "repair_type", "repair_reason", "work_done", "team", "result", "well_number",
                "downtime", "costs", "period", "cumulative_oil", "deviation"
            }
        }
        # Получние модели и допустимых полей
        model_class = model_map.get(form_type)
        allowed_fields = form_fields.get(form_type)

        if not model_class or not allowed_fields:
            return jsonify({"error": f"Неизвестный тип формы: {form_type}"}), 400
        # Поля, содержащие даты
        date_fields = {"measurement_date", "start_date", "end_date"}
        # Получение идентификатора пользователя из JWT
        created_by = get_jwt_identity()
        # Обработка каждой записи в отчете
        for entry in report_data:
            # Фильтрация полей по разрешенным
            filtered_entry = {key: entry[key] for key in allowed_fields if key in entry}
            # Преобразование дат
            for date_field in date_fields:
                if date_field in filtered_entry:
                    filtered_entry[date_field] = parse_date(filtered_entry[date_field])
            # Добавление информации о создателе
            filtered_entry["created_by"] = created_by
            # Создание и сохранение записи
            record = model_class(**filtered_entry)
            db.session.add(record)
        # Фиксация изменений в БД
        db.session.commit()
        return jsonify({"message": f"Отчет '{form_type}' успешно сохранён в базу данных."}), 200

    except Exception as e:
        # Откат измененеий при ошибке
        db.session.rollback()
        return jsonify({"error": f"Ошибка сохранения: {str(e)}"}), 500

# Вспомогательные функции
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT").date() if date_str else None
    except Exception:
        return None

def parse_float(value):
    try:
        return float(value) if value not in [None, ""] else None
    except Exception:
        return None

def parse_int(value):
    try:
        return int(value) if value not in [None, ""] else None
    except Exception:
        return None