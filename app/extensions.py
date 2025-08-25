from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio   import SocketIO

# Instancia de SQLAlchemy para importar en otros módulos
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*", logger=False, engineio_logger=False)  # mensaje_queue para Redis si lo usas
