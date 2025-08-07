from app.models.usuario import Usuario
from flask import request, session
from app.services.jwt_service import generar_token, verificar_token
from app.extensions import db


# Servicio para gestionar los usuarios
def gestionar_usuarios_admin_service():
    token = session.get('jwt')

      # Si no hay token en sesión, intenta obtenerlo del header Authorization
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    
    if not token:
        return {"success": False, "message": "Token  no enviado."}
    
    
    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario_admin = Usuario.query.filter_by(usuario_id=usuario_id).first()

    if not usuario_admin:
        return{"success": False, "message": "Usuario no encontrado"}
    
    if usuario_admin.id_rol != 3:
        return{"success": False, "message": "No tienes permisos de administrador"}
    
    # Traemos a todos los usuarios
    usuarios = Usuario.query.all()

    # Los guardamos en el array lista_usuarios
    lista_usuarios = []

    for usuario in usuarios:
        lista_usuarios.append({
            "usuario_id": usuario.usuario_id,
            "fecha_registro": usuario.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")  if usuario.fecha_registro else None,
            "correo": usuario.correo,
            "estado": usuario.estado,
            "token_recuperacion": usuario.token_recuperacion,
            "intentos_fallidos": usuario.intentos_fallidos,
            "bloqueado_hasta": usuario.bloqueado_hasta.strftime("%Y-%m-%d %H:%M:%S") if usuario.bloqueado_hasta else None,
            "id_rol": usuario.id_rol
        })

    return {"success": True, "usuarios": lista_usuarios}


# Servicio para deshabilitar cuentas de usuarios
def deshabilitar_cuentas_admin_service(data):
    token = session.get('jwt')

      # Si no hay token en sesión, intenta obtenerlo del header Authorization
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return {"success": True, "message": "Token no enviado"}
    
    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario_admin = Usuario.query.filter_by(usuario_id=usuario_id).first()
    
    if not usuario_admin:
        return{"success": False, "message": "Usuario no encontrado"}
    
    if usuario_admin.id_rol != 3:
        return{"success": False, "message": "No tienes permisos de administrador"}

    
    usuario_id = data.get("usuario_id")

    usuario = Usuario.query.filter_by(usuario_id=usuario_id).first()

    # Validamos si existe el usuario
    if not usuario:
        return {"success": False, "message": "No hay ningun usuario"}
    
    # Verificamos si el usuario ya esta deshabilitado
    if usuario.estado == "deshabilitado":
        return{"success": False, "message": "El usuario ya esta deshabilitado"}
    
    # En caso de estar activo lo cambiamos a deshabilitado
    if usuario.estado == "activo":
        usuario.estado = "deshabilitado"
        db.session.commit()

        return {"success": True, "message": f"El usuario con ID {usuario_id} ha sido deshabilitado"}

