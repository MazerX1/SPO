from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from backend.routes.data import data_bp

app = Flask(__name__)

jwt = JWTManager(app)

# Разрешение CORS
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
CORS(data_bp)

app.register_blueprint(data_bp, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)
