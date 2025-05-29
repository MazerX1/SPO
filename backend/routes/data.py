from flask_jwt_extended import jwt_required
# Работа с базами данных
from sqlalchemy import inspect
from flask import Blueprint, request, jsonify
import psycopg2
# Модули и расширения приложения
from backend.extensions import db
from backend.models.models import Form4Measurement, Form10Repair, Form13Dynamics, FormNew
# Словарь соответствия форм и модулей
form_models = {
    '4': Form4Measurement,
    '10': Form10Repair,
    '13': Form13Dynamics
}
# Словарь перевода названий столбцов
column_translations = {
    'month': 'Месяц',
    'measurement_date': 'Дата замера',
    'liquid_flow': 'Дебит жидкости (м³/сут)',
    'oil_flow': 'Дебит нефти (т/сут)',
    'water_cut': 'Обводненность (%)',
    'notes': 'Примечание',
    'mode': 'Режим работы',
    'pressure': 'Давление (МПа)',
    'exploitation_coefficient': 'Коэффициент эксплуатации',

    'start_date': 'Дата начала ремонта',
    'end_date': 'Дата окончания ремонта',
    'repair_type': 'Вид ремонта',
    'repair_reason': 'Причина ремонта',
    'work_done': 'Выполненные работы',
    'team': 'Бригада',
    'result': 'Результат ремонта',
    'well_number': 'Номер скважины',
    'downtime': 'Время простоя (часы)',
    'costs': 'Затраты (руб)',

    'period': 'Период',
    'oil_flow': 'Добыча нефти (т/сут)',
    'liquid_flow': 'Добыча жидкости (м³/сут)',
    'water_cut': 'Обводненность (%)',
    'cumulative_oil': 'Накопленная добыча нефти (т)',
    'deviation': 'Отклонение (%)',
}
# Создание Blueprint для работы с данными
data_bp = Blueprint('data_bp', __name__)

# Получение отчетов из PostgreSQL с фильтрацией по дате
@data_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    # Извлечение параметров из запроса
    username = request.args.get('username')
    password = request.args.get('password')
    dbname = request.args.get('dbname')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    print(f"Received request with username={username}, dbname={dbname}, start_date={start_date}, end_date={end_date}")
    # Проверка обязательных параметров
    if not username or not password or not dbname:
        print("Invalid connection parameters")
        return jsonify({'error': 'Invalid connection parameters'}), 400

    try:
        print("Connecting to the database...")
        # Подключение к PostgreSQL
        connection = psycopg2.connect(
            dbname=dbname,
            user=username,
            password=password,
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        # Выполнение запроса с фильтрацией по дате
        query = """
            SELECT * FROM reports
            WHERE (%s IS NULL OR measurement_date >= %s)
            AND (%s IS NULL OR measurement_date <= %s)
        """

        cursor.execute(query, (start_date, start_date, end_date, end_date))
        # Формирование результата
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        connection.close()

        print("Query executed successfully")

        return jsonify({'rows': data, 'columns': columns})

    except Exception as error:
        print(f"Error occurred: {error}")
        return jsonify({'error': str(error)}), 500

# Получение списка таблиц в указанной базе данных PostgreSQL
@data_bp.route('/load_tables', methods=['POST'])
@jwt_required()
def load_tables():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    dbname = data.get("dbname")

    conn_str = f"postgresql://{username}:{password}@localhost:5432/{dbname}"
    print("Подключение:", conn_str)

    try:
        from sqlalchemy import create_engine, inspect
        # Создание подключения через SQLAlchemy
        engine = create_engine(conn_str)
        # Получение списка таблиц
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return jsonify({"tables": tables})
    except Exception as e:
        import traceback
        print("Ошибка при подключении к базе:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Загрузка данных для указанной формы
@data_bp.route('/load_form_data', methods=['POST'])
@jwt_required()
def load_form_data():
    creds = request.get_json()
    form_id = creds.get('form')

    model = form_models.get(form_id)
    if not model:
        return jsonify({"error": "Неизвестная форма"}), 400

    try:
        # Получение данных из БД
        query = db.session.query(model).limit(100)
        rows = []
        for obj in query.all():
            row = {col.name: getattr(obj, col.name) for col in model.__table__.columns}
            rows.append(row)

        columns = [col.name for col in model.__table__.columns]

        return jsonify({
            "columns": columns,
            "rows": rows
        })
    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({"error": str(e)}), 500
# Получение переведенных названий столбцов для формы
@data_bp.route('/form_columns/<form_id>')
@jwt_required()
def get_form_columns(form_id):
    model = form_models.get(form_id)
    if not model:
        return jsonify({'error': 'Форма не найдена'}), 404

    mapper = inspect(model)
    # Формирование списка слобцов с переводами
    columns = []
    for column in mapper.columns:
        if column.key != 'id':
            columns.append({
                'field': column.key,
                'label': column_translations.get(column.key, column.key)
            })

    return jsonify({'columns': columns})


