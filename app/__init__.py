# app/__init__.py

from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_cors import CORS
from app.extensions import db, migrate, socketio

def create_app():
    # 1) Instancia de Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    
    # 🔹 Habilitar CORS en toda la app
    CORS(app, resources={r"/*": {
        "origins": ["http://127.0.0.1:5000", "http://localhost:5000"], 
        "supports_credentials": True # Esto es CLAVE para que Flask-Login funcione con AJAX
    }})

    # 2) Inicializa extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # 3) Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'web.iniciar_sesion'
    login_manager.init_app(app)

    from app.models.usuario import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # 4) Registra blueprints
    from app.routes.web import web as web_bp
    app.register_blueprint(web_bp)

    from app.services.mensajeria import mensajeria_bp
    app.register_blueprint(mensajeria_bp)

    from app.services_movil.mensajeria_routes import mensajeria_movil_bp
    app.register_blueprint(mensajeria_movil_bp)
    
    from app.api.users import users_api
    app.register_blueprint(users_api, url_prefix="/api")

    # 5) Crea tablas y lista rutas (opcional en dev)
    with app.app_context():
        db.create_all()


    return app
