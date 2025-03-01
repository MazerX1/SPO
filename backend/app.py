from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

from backend.extensions import db
#from backend.routes.auth import auth_bp
from backend.routes.reports import routes_bp
from backend.routes.data import data_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/production_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db.init_app(app)

# Инициализация миграций
migrate = Migrate(app, db)

jwt = JWTManager(app)

# Разрешение CORS
CORS(app)
CORS(data_bp)
# Регистрируем Blueprint с маршрутами
app.register_blueprint(routes_bp, url_prefix='/api')
#app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(data_bp, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)
