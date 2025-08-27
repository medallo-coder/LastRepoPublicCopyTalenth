from flask import Blueprint, request, jsonify
from app.services.autenticacion import registrar_usuario_service, iniciar_sesion_service, cerrar_sesion_service
from app.services_desktop.autenticacion import iniciar_sesion_admin_service, registrar_admin_service, cerrar_sesion_admin_service
from app.services_desktop.gestion_publicaciones import  gestion_publicaciones_admin_service, eliminar_publicaciones_admin_service
from app.services_desktop.gestionar_usuarios import gestionar_usuarios_admin_service, deshabilitar_cuenta_global_service
from app.services_desktop.perfil_usuarios  import perfil_usuarios_admin_service
from app.services_desktop.gestion_reportes import gestion_reportes_admin_service
from app.services_desktop.gestion_admin import cambiar_contrasena_admin_service, deshabilitar_cuenta_admin_usu_service
from app.services_desktop.gestion_admin import datos_admin_service, deshabilitar_cuentas_admin_service
from app.services_desktop.gestionar_usuarios import datos_expertos_service, datos_clientes_service

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



#--------------------RUTAS DE DESKTOP---------------------#
# Ruta para registrarse como admin
@users_api.route('/registrar_sesion_admin', methods=['POST'])
def registrar_sesion_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = registrar_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)

# Ruta para iniciar sesion como admin
@users_api.route('/iniciar_sesion_admin', methods=['POST'])
def iniciar_session_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = iniciar_sesion_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 401)

# Ruta para cerrar sesion en el apartado admin
@users_api.route('/cerrar_sesion_admin', methods=['POST'])
def cerrar_sesion_admin():
    resultado = cerrar_sesion_admin_service()
    return jsonify(resultado), 200

# Ruta para gestionar a los usuarios 
@users_api.route('/gestion_usuarios_admin', methods=['POST'])
def gestionar_usuarios_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado= gestionar_usuarios_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)


# Ruta para deshabilitar las cuentas de los usuarios
@users_api.route('/deshabilitar_cuentas_admin', methods=['POST'])
def deshabilitar_cuentas_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = deshabilitar_cuentas_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)

# Ruta para ver los perfiles de los usuarios
@users_api.route('/perfil_usuarios_admin', methods=['POST'])
def perfil_usuarios_admin():
    resultado = perfil_usuarios_admin_service()
    return jsonify(resultado), (200 if resultado["success"] else 400)

# Ruta para ver las publicaciones de los usuarios
@users_api.route('/gestion_publicaciones_admin', methods=['POST'])
def gestion_publicaciones_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = gestion_publicaciones_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400) 

# Ruta para eliminar publicaciones de los usuarios 
@users_api.route('/eliminar_publicaciones_admin', methods=['POST'])
def eliminar_publicaciones_admin():
    data= request.get_json() if request.is_json else request.form.to_dict() 
    resultado = eliminar_publicaciones_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400)   

@users_api.route('/gestion_reportes_admin', methods=['POST'])
def gestion_reportes_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = gestion_reportes_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400) 

@users_api.route('/cambiar_contraseña_admin', methods=['POST'])
def cambiar_contraseña_admin():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = cambiar_contrasena_admin_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400)


@users_api.route('/deshabilitar_cuenta_admin_us', methods=['POST'])
def deshabilitar_cuenta_admin_usu():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = deshabilitar_cuenta_admin_usu_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400)

@users_api.route('/datos_admin', methods=['POST'])
def datos_admin_():
    resultado = datos_admin_service()
    return jsonify(resultado), (200 if resultado["success"]else 400)

@users_api.route('/datos_expertos', methods=['POST'])
def datos_expertos():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = datos_expertos_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400)

@users_api.route('/datos_clientes', methods=['POST'])
def datos_clientes():
    data = request.get_json() if request.is_json else request.form.to_dict()
    resultado = datos_clientes_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400)


@users_api.route('/deshabilitar_cuenta_global', methods=['POST'])
def deshabilitar_cuenta_global():
    data = request.get_json() if request.is_json else request.form.to_dict()
    resultado = deshabilitar_cuenta_global_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400)