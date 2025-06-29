
from .index import index_bp  # Importa el Blueprint de index

#se añadieron estas librerias (mensajeria)
from flask import Blueprint
from .web import web as web_bp
from app.services.mensajeria import mensajeria_bp  # 👈 Asegúrate de importar esto

#Se añadio register_routes para la interfaz de mensajeria
def register_routes(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(web_bp)
    app.register_blueprint(mensajeria_bp)  # 👈 Regístralo aquí