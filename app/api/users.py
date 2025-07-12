from flask import Blueprint, request, jsonify
from app.services.autenticacion import registrar_usuario_service, iniciar_sesion_service, cerrar_sesion_service
from app.services_desktop import iniciar_sesion_admin_service, registrar_admin_service, cerrar_sesion_admin_service, gestionar_usuarios_admin_service, deshabilitar_cuentas_admin_service
from app.services_desktop import perfil_usuarios_admin_service, gestion_publicaciones_admin_service
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

@users_api.route('/registrar_sesion_admin', methods=['POST'])
def registrar_sesion_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = registrar_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)

@users_api.route('/iniciar_sesion_admin', methods=['POST'])
def iniciar_session_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = iniciar_sesion_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 401)

@users_api.route('/cerrar_sesion_admin', methods=['POST'])
def cerrar_sesion_admin():
    resultado = cerrar_sesion_admin_service()
    return jsonify(resultado), 200

@users_api.route('/gestion_usuarios_admin', methods=['POST'])
def gestionar_usuarios_admin():
    resultado= gestionar_usuarios_admin_service()
    return jsonify(resultado), (200 if resultado["success"] else 400)

@users_api.route('/deshabilitar_cuentas_admin', methods=['POST'])
def deshabilitar_cuentas_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = deshabilitar_cuentas_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)

@users_api.route('perfil_usuarios_admin', methods=['POST'])
def perfil_usuarios_admin():
    resultado = perfil_usuarios_admin_service()
    return jsonify(resultado), (200 if resultado["success"] else 400)

@users_api.route('gestion_publicaciones_admin', methods=['POST'])
def gestion_publicaciones_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = gestion_publicaciones_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400) 