# app/routes/__init__.py

from flask import Blueprint
from .web import web as web_bp
from app.services.mensajeria import mensajeria_bp  # Este es tu segundo blueprint

def register_routes(app):
    app.register_blueprint(web_bp)
    app.register_blueprint(mensajeria_bp)
