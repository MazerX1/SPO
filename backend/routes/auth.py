# Работа с базой данных SQLite
import sqlite3
# Компоненты Flask
from flask import Blueprint, request, jsonify, g
# Аутентификация JWT
from flask_jwt_extended import create_access_token
# Хеширование паролей
from werkzeug.security import generate_password_hash, check_password_hash
# Создание Blueprint для аутентификации
auth_bp = Blueprint('auth_bp', __name__)
# Путь к файлу базы данных пользователей
DATABASE = 'users.db'

# Функция для получения соединения с БД (SQLite)
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db
# Закрытие соеднинения с БД после завершения запроса
@auth_bp.teardown_app_request
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()
# Регистрация
@auth_bp.route('/register', methods=['POST'])
def register():
    # Получение данных из запроса
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    db = get_db()
    # Проверка существования пользователя
    if db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone():
        return jsonify({"message": "User already exists"}), 400
    # Хеширование пароля и сохранение пользователя
    hashed_password = generate_password_hash(password)
    db.execute(
        'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
        (username, hashed_password, role)
    )
    db.commit()
    return jsonify({"message": "User registered successfully"}), 201
# Авторизация
@auth_bp.route('/login', methods=['POST'])
def login():
    # Получение учетных данных
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Проверка учетных данных
    if not check_user_credentials(username, password):
        return jsonify({"message": "Invalid credentials"}), 401
    # Создание JWT токена с ролью пользователя
    role = get_user_role(username)
    token = create_access_token(identity=username, additional_claims={"role": role})
    return jsonify(access_token=token, role=role), 200
# Проверка соответствия логина и пароля
def check_user_credentials(username, password):
    db = get_db()
    user = db.execute('SELECT password FROM users WHERE username = ?', (username,)).fetchone()
    return user and check_password_hash(user['password'], password)
# Получение роли пользователя
def get_user_role(username):
    db = get_db()
    user = db.execute('SELECT role FROM users WHERE username = ?', (username,)).fetchone()
    return user['role'] if user else None