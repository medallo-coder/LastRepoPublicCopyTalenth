from app.models.usuario import Usuario
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, request
from app.services_movil.jwt_service import verificar_token
from app.extensions import db


# Servicio para cambiar la contraseña
def cambiar_contrasena_usuario_service(data):

    # Obtener token de la sesión y verificar
    # Si no hay token en sesión, intenta obtenerlo del header Authorization
    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        return {"success": True, "message": "Token no enviado"}

        
    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get('usuario_id')

    # Obtener el usuario de la base de datos
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}
    
    if usuario.id_rol not in(1,2):
        return {"success": False, "message": "Tienes que ser usuario o experto"}
    
    if usuario.estado == "deshabilitado":
        return{"success": False, "message": "Tu usuario esta deshabilitado"}

    actual_contrasena = data.get('actual_contrasena')
    nueva_contrasena = data.get('nueva_contrasena')
    confirmar_contrasena = data.get('confirmar_contrasena')

    # Verificar que todos los campos estén presentes
    if not actual_contrasena or not nueva_contrasena or not confirmar_contrasena:
        return {"success": False, "message": "Todos los campos son obligatorios."}

    # Verificar que las contraseñas nuevas coincidan
    if nueva_contrasena != confirmar_contrasena:
        return {"success": False, "message": "Las contraseñas no coinciden."}

    # Verificar que la nueva contraseña tenga al menos 6 caracteres
    if len(nueva_contrasena) < 6:
        return {"success": False, "message": "La contraseña debe tener al menos 6 caracteres."}

    

    # Verificar la contraseña actual
    if not check_password_hash(usuario.contrasena, actual_contrasena):
        return {"success": False, "message": "La contraseña actual es incorrecta."}

    # Si todo es correcto, actualizamos la contraseña
    usuario.contrasena = generate_password_hash(nueva_contrasena)
    db.session.commit()

    return {"success": True, "message": "Contraseña actualizada correctamente."}

# Solo valida contraseña
def validar_contrasena_usuario_service(data):
    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}

    contrasena = data.get("contrasena")
    if not contrasena:
        return {"success": False, "message": "La contraseña es obligatoria."}

    if not check_password_hash(usuario.contrasena, contrasena):
        return {"success": False, "message": "La contraseña es incorrecta."}

    return {"success": True, "message": "Contraseña válida."}


# Aquí sí se deshabilita
def deshabilitar_cuenta_usuario_service(data):
    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}

    usuario.estado = "deshabilitado"
    db.session.commit()

    session.pop('jwt', None)
    return {"success": True, "message": "Tu cuenta ha sido deshabilitada correctamente."}




def datos_usuario_service():
     # Obtener token desde la sesión
    token = session.get('jwt')

      # Si no hay token en sesión, intenta obtenerlo del header Authorization
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]


   
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get('usuario_id')
    usuario = Usuario.query.get(usuario_id)
   

    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}
    
    # Obtener la fecha de registro y formatearla
    fecha_registro = usuario.fecha_registro
    fecha_formateada = fecha_registro.strftime("%B de %Y")  # Ejemplo: Noviembre de 2020

    rol = usuario.rol
    perfil= usuario.perfiles

    datos_usuario = {
        "usuario_id": usuario.usuario_id,
        "nombre": perfil.primer_nombre.title(),
        "apellido": perfil.primer_apellido.title(),
        "nombre_completo": f"{perfil.primer_nombre.title()} {perfil.primer_apellido.title()}",
        "fecha_registro": fecha_formateada,
        "rol_usuario": usuario.id_rol,          # 👈 clave consistente con inicio_service
        "rol": rol.tipo_rol.title()             # 👈 opcional, si quieres el nombre del rol
    }

    return {"success": True, "usuario": datos_usuario}