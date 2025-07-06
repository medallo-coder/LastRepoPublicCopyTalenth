from app.extensions import db
from app.models.guardados import Guardados
from app.models.publicaciones import Publicaciones
from app.services.autenticacion import obtener_usuario_id_autenticado

def guardar_publicacion_service(publicacion_id):
    usuario_id = obtener_usuario_id_autenticado()
    if not usuario_id:
        return {"success": False, "message": "No estás autenticado."}

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



def obtener_guardados_service():
    usuario_id = obtener_usuario_id_autenticado()
    if not usuario_id:
        return []

    guardados = Guardados.query.filter_by(usuario_id=usuario_id).all()
    return [g.publicacion for g in guardados]


def eliminar_guardado_service(publicacion_id):
    usuario_id = obtener_usuario_id_autenticado()
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
