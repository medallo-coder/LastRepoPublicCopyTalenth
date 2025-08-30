from flask import session
from app.models.usuario import Usuario
from app.services_movil.jwt_service import verificar_token
from app.extensions import db

def cambiar_rol_a_experto_service():
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado = verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": resultado["message"]}

    usuario_id = resultado["payload"].get("usuario_id")
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}

    if usuario.id_rol == 1:
        return {"success": False, "message": "Ya eres un experto."}

    usuario.id_rol = 1
    try:
        db.session.commit()
        session['rol'] = usuario.id_rol  # ✅ ¡Actualizar el rol en la sesión!
        return {"success": True, "message": "¡Ahora eres un experto!"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al actualizar rol: {str(e)}"}


#cambiar rol a cliente 

def cambiar_rol_a_cliente_service():
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado = verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": resultado["message"]}

    usuario_id = resultado["payload"].get("usuario_id")
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}

    if usuario.id_rol == 2:
        return {"success": False, "message": "Ya eres un cliente."}

    usuario.id_rol = 2
    try:
        db.session.commit()
        session['rol'] = usuario.id_rol  # ✅ ¡Actualizar el rol en la sesión!
        return {"success": True, "message": "¡Ahora eres un cliente!"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al actualizar rol: {str(e)}"}

def verificar_rol(token):
    if not token:
        return None

    resultado = verificar_token(token)
    if not resultado.get("valid"):
        return None

    usuario_id = resultado["payload"].get("usuario_id")
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return None

    return usuario.id_rol  # Ej: 1 = Experto, 2 = Cliente