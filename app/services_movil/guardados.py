from app.extensions import db
from flask import request, session
from app.models.guardados import Guardados
from app.models.publicaciones import Publicaciones
from app.services_movil.autenticacion import obtener_usuario_id_autenticado
from app.models.usuario import Usuario
from app.services_movil.jwt_service import verificar_token

def guardar_publicacion_service(data):
   
    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return {"success": False, "message": "Token no enviado."}

    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario = Usuario.query.filter_by(usuario_id=usuario_id).first()

    if not usuario:
        return{"success": False, "message": "Usuario no encontrado"}
    
    publicacion_id = data.get('publicacion_id')

    # Verifica que la publicación exista
    publicacion = Publicaciones.query.get(publicacion_id)
    
    if not publicacion:
        return {"success": False, "message": "Publicación no encontrada."}

    # Verifica si ya fue guardada
    existe = Guardados.query.filter_by(usuario_id=usuario_id, publicacion_id=publicacion_id).first()
    if existe:
        return {"success": False, "message": "La publicación ya estaba guardada."}

    # Crear el registro
    nuevo_guardado = Guardados(usuario_id=usuario_id, publicacion_id=publicacion_id)
    db.session.add(nuevo_guardado)
    try:
        db.session.commit()
        return {"success": True, "message": "Publicación guardada exitosamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al guardar: {str(e)}"}


from sqlalchemy.orm import joinedload

from sqlalchemy.orm import joinedload

def obtener_guardados_service():
    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return {"success": False, "message": "Token no enviado."}

    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario = Usuario.query.filter_by(usuario_id=usuario_id).first()

    if not usuario:
        return{"success": False, "message": "Usuario no encontrado"}
  

    guardados = (
        Guardados.query
        .filter_by(usuario_id=usuario_id)
        .options(
            joinedload(Guardados.publicacion)
            .joinedload(Publicaciones.usuario)
            .joinedload(Usuario.perfiles)
        )
        .all()
    )

    return {
        "success": True,
        "message": "Guardados obtenidos correctamente",
         "data": [g.to_dict() for g in guardados]
    }


def eliminar_guardado_service(data):

    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return {"success": False, "message": "Token no enviado."}

    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario = Usuario.query.filter_by(usuario_id=usuario_id).first()

    if not usuario:
        return{"success": False, "message": "Usuario no encontrado"}
  

    publicacion_id = data.get('publicacion_id')
    
    if not usuario_id:
        return {"success": False, "message": "No estás autenticado."}

    guardado = Guardados.query.filter_by(usuario_id=usuario_id, publicacion_id=publicacion_id).first()
    if not guardado:
        return {"success": False, "message": "No encontrado."}

    db.session.delete(guardado)
    try:
        db.session.commit()
        return {"success": True, "message": "Eliminado correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al eliminar: {str(e)}"}
