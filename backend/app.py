# Модули Flask (обработка CORS, аутентификация JWT)
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
# Собственные модули
from backend.extensions import db
from backend.routes.auth import auth_bp
from backend.routes.data import data_bp
from backend.routes.report_routes import report_bp
# Создание эземпляра Flask приложения
app = Flask(__name__)
# Путь к файлу базы данных
db_path = r'C:\Zhenya\Dev\SPO\backend\reports.db'
# Конфигурация приложения
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
# Инициализация JWT менеджера
jwt = JWTManager(app)
# Инициализация базы данных
db.init_app(app)
# Настройка CORS с ограничением по домену и маршрутам
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)
# Регистрация маршрутов с префиксом /api
app.register_blueprint(data_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(report_bp)

if __name__ == '__main__':
    app.run(debug=True)
