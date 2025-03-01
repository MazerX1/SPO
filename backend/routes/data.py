from flask import Blueprint, jsonify
from sqlalchemy import text
from backend.extensions import db

data_bp = Blueprint("data", __name__)

@data_bp.route("/data", methods=["GET"])
def get_data():
    try:
        query = text("SELECT * FROM reports LIMIT 10")  # Пример запроса
        result = db.session.execute(query)

        # Получаем названия колонок
        columns = result.keys()

        # Преобразуем результат в список словарей
        data = [dict(zip(columns, row)) for row in result.fetchall()]

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
