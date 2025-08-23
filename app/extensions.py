from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instancia de SQLAlchemy para importar en otros módulos
db = SQLAlchemy()
migrate = Migrate()
