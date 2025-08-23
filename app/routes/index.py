from flask import Blueprint, render_template
from app.services.configuracion import obtener_datos_usuario_service

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def inicio():
    resultado = obtener_datos_usuario_service()
    primer_nombre = resultado.get('primer_nombre', 'Usuario Invitado')
    return render_template('index.html', primer_nombre=primer_nombre)
