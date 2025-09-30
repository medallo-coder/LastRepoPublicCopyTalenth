from flask import Blueprint, request, jsonify, redirect
from app.services_desktop.autenticacion import iniciar_sesion_admin_service, registrar_admin_service, cerrar_sesion_admin_service 
from app.services_desktop.gestion_publicaciones import  gestion_publicaciones_admin_service, eliminar_publicaciones_admin_service
from app.services_desktop.gestionar_usuarios import gestionar_usuarios_admin_service, deshabilitar_cuenta_global_service
from app.services_desktop.perfil_usuarios  import perfil_usuarios_admin_service
from app.services_desktop.gestion_reportes import gestion_reportes_admin_service
from app.services_desktop.gestion_admin import cambiar_contrasena_admin_service, deshabilitar_cuenta_admin_usu_service
from app.services_desktop.gestion_admin import datos_admin_service, deshabilitar_cuentas_admin_service
from app.services_desktop.gestionar_usuarios import datos_expertos_service, datos_clientes_service
from app.services_movil.autenticacion import registrar_usuario_service, iniciar_sesion_service, cerrar_sesion_service, obtener_usuario_id_autenticado
from app.services_movil.inicio import inicio_service
from app.services_movil.gestion_usuarios import datos_usuario_service, cambiar_contrasena_usuario_service, deshabilitar_cuenta_usuario_service, validar_contrasena_usuario_service
from app.services_movil.guardados import guardar_publicacion_service, obtener_guardados_service, eliminar_guardado_service
from app.services_movil.reporte import guardar_reporte_service
from app.services_movil.publicaciones import guardar_publicacion_usuario_service
from app.services_movil.configuracion import enviar_link_recuperacion_service, restablecer_contraseña_service
from flask import Blueprint, request



# Define the Blueprint for the API
users_api = Blueprint('users_api', __name__)



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
         # obtener el token del header Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]  # quitar "Bearer "
    else:
        return {"success": False, "message": "Token no proporcionado"}, 400

    resultado = cerrar_sesion_admin_service(token)
    return resultado

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



#------------------RUTAS DE MOVIL-------------------------------------------

@users_api.route('/', methods=['GET'])
def inicio():
    resultado = inicio_service()
    return jsonify(resultado), (200 if resultado["success"] else 400)


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
        # obtener el token del header Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]  # quitar "Bearer "
    else:
        return {"success": False, "message": "Token no proporcionado"}, 400

    resultado = cerrar_sesion_service(token)
    return resultado

@users_api.route('/datos_usuario', methods=['POST'])
def datos_usuario_():
    resultado = datos_usuario_service()
    return jsonify(resultado), (200 if resultado["success"]else 400)


@users_api.route('/cambiar_contraseña_usuario', methods=['POST'])
def cambiar_contraseña_usuario():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = cambiar_contrasena_usuario_service(data)
    return jsonify(resultado), (200 if resultado["success"]else 400)

@users_api.route('/validar_contrasena_usuario', methods=['POST'])
def validar_contrasena_usuario():
    data = request.get_json() if request.is_json else request.form.to_dict()
    resultado = validar_contrasena_usuario_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)


@users_api.route('/deshabilitar_cuenta_usuario', methods=['POST'])
def deshabilitar_cuenta_usuario():
    data = request.get_json() if request.is_json else request.form.to_dict()
    resultado = deshabilitar_cuenta_usuario_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)


# Ruta para la sección de guardados (requiere sesión)
@users_api.route('/guardar-publicacion', methods=['POST'])
def guardar_publicacion():
    data= request.get_json() if request.is_json else request.form.to_dict()  
    resultado = guardar_publicacion_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)
    

#Ruta de publicaciones guardadas
@users_api.route('/mis_guardados', methods=['GET'])
def guardados():
    resultado = obtener_guardados_service()
    return jsonify(resultado), (200 if resultado["success"] else 400)


# Ruta para eliminar un guardado@web.route('/mis-guardados/eliminar')
@users_api.route('/mis-guardados/eliminar', methods=['POST'])
def eliminar_guardado():
    data= request.get_json() if request.is_json else request.form.to_dict() 
    resultado = eliminar_guardado_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)



@users_api.route('/guardar_reporte', methods=['POST'])
def guardar_reporte():
    data= request.get_json() if request.is_json else request.form.to_dict() 
    resultado = guardar_reporte_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)

@users_api.route('/publicaciones', methods=['POST'])
def publicaciones():
    data= request.get_json() if request.is_json else request.form.to_dict() 
    resultado = guardar_publicacion_usuario_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)


# Ruta para enviar el enlace de recuperación de contraseña
# Esta ruta se activa al enviar el formulario de recuperación
@users_api.route('/recuperar_contraseña', methods=['POST'])
def recuperar_contraseña():
        data= request.get_json() if request.is_json else request.form.to_dict()
        resultado = enviar_link_recuperacion_service(data)
        return jsonify(resultado), (200 if resultado["success"] else 400)

# Ruta para restablecer la contraseña
# Esta ruta se activa al hacer clic en el enlace enviado al correo
@users_api.route('/formulario_movil', methods=['GET', 'POST'])
def formulario_movil():
        token = request.args.get("token")  # lo saca de la URL
        if not token:
            return jsonify({"success": False, "message": "Token faltante"}), 400
        
        # Aquí puedes decidir:
        # 1. Redirigir a la app móvil con el token
        return redirect(f"http://127.0.0.1:8550/cambiar_contrasena?token={token}")



# Ruta para restablecer la contraseña
# Esta ruta se activa al hacer clic en el enlace enviado al correo
@users_api.route('/restablecer_contraseña_datos', methods=['POST'])
def restablecer_contraseña_datos():
    data= request.get_json() if request.is_json else request.form.to_dict()
    resultado = restablecer_contraseña_service(data)
    return jsonify(resultado), (200 if resultado["success"] else 400)
 



