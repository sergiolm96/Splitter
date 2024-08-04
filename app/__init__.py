from flask import Flask
from .init_db import init_db
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'admin'

    # Registrar blueprint
    app.register_blueprint(main_bp)

    # Inicializar la base de datos
    with app.app_context():
        init_db()

    return app
