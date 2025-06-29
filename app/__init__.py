from flask import Flask
from app.extensions import db, migrate
from app.routes.index import index_bp
from app.api.users import users_api as api_bp
from app.routes.web import web as web_bp
from app.models.roles import Roles
from app.models.usuario import Usuario
from app.models.subcategorias import Subcategorias
from flask_login import LoginManager
from app.services.mensajeria import mensajeria_bp
from app.services.rol_service import verificar_rol
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuración base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dbtalento'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clave_super_segura_123'

    # Inicialización de extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Configuración LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(web_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(mensajeria_bp)

    # Inyección de rol en plantillas
    @app.context_processor
    def inject_rol():
        return dict(id_rol=verificar_rol())

    # Crear tablas
    with app.app_context():
        from app.models import usuario
        try:
            db.create_all()
            print("✅ Conexión a la base de datos correcta.")
        except Exception as e:
            print(f"❌ Error al crear las tablas: {e}")

    from app import models
    return app
