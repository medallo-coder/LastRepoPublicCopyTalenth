from app.models.usuario import Usuario
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, request
from app.services.jwt_service import verificar_token
from app.extensions import db


# Servicio para cambiar la contraseña
def cambiar_contrasena_admin_service(data):

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
    
    if usuario.id_rol !=3:
        return {"success": False, "message": "Tienes que ser admin"}
    
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