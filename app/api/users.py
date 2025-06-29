from flask import Blueprint, request, jsonify
from app.services.autenticacion import registrar_usuario_service, iniciar_sesion_service, cerrar_sesion_service

# Define the Blueprint for the API
users_api = Blueprint('users_api', __name__)

# Ruta para registrar usuario
@users_api.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    data = request.get_json() if request.is_json else request.form.to_dict()
    resultado = registrar_usuario_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)

# Ruta para iniciar sesión
@users_api.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    data = request.get_json() if request.is_json else request.form.to_dict()
    resultado = iniciar_sesion_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 401)

# Ruta para cerrar sesión
@users_api.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion():
    resultado = cerrar_sesion_service()
    return jsonify(resultado), 200
