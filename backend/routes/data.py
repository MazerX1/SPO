import traceback
from sqlalchemy import create_engine, inspect
from flask import Blueprint, request, jsonify, current_app
import psycopg2

data_bp = Blueprint('data_bp', __name__)

# Получение списка таблиц
@data_bp.route('/load_tables', methods=['POST'])
def load_tables():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    dbname = data.get("dbname")

    conn_str = f"postgresql://{username}:{password}@localhost:5432/{dbname}"
    print("Подключение:", conn_str)

    try:
        engine = create_engine(conn_str)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return jsonify({"tables": tables})
    except Exception as e:
        print("Ошибка при подключении к базе:", e)
        return jsonify({"error": str(e)}), 500

# Получение данных конкретной таблицы
@data_bp.route('/load_table_data', methods=['POST'])
def load_table_data():
    creds = request.get_json()
    username = creds.get('username')
    password = creds.get('password')
    dbname = creds.get('dbname')
    table = creds.get('table')

    try:
        # Подключение к базе данных
        print(f"Подключаемся к базе данных: {dbname} с пользователем {username}")
        conn = psycopg2.connect(
            dbname=dbname,
            user=username,
            password=password,
            host="localhost"
        )
        cur = conn.cursor()

        # Выполнение запроса
        print(f"Запрашиваем таблицу: {table}")
        cur.execute(f'SELECT * FROM "{table}" LIMIT 100')
        colnames = [desc[0] for desc in cur.description]
        rows = [dict(zip(colnames, row)) for row in cur.fetchall()]

        cur.close()
        conn.close()

        # Возвращаем данные
        return jsonify({
            "columns": colnames,
            "rows": rows
        })
    except Exception as e:
        # Логируем ошибку
        print(f"Ошибка: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
