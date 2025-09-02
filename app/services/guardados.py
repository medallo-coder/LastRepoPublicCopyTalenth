from app.extensions import db
from app.models.guardados import Guardados
from app.models.publicaciones import Publicaciones
from app.services.autenticacion import obtener_usuario_id_autenticado
from app.services.configuracion import obtener_datos_usuario_service
from app.models.usuario import Usuario
from sqlalchemy.exc import IntegrityError


def guardar_publicacion_service(publicacion_id):
    usuario = obtener_datos_usuario_service()
    usuario_id = usuario.get("usuario_id") if usuario else obtener_usuario_id_autenticado()

    if not usuario_id:
        return {"success": False, "message": "No estás autenticado.", "guardado": False}

    publicacion = Publicaciones.query.get(publicacion_id)
    if not publicacion:
        return {"success": False, "message": "Publicación no encontrada.", "guardado": False}

    guardado_existente = Guardados.query.filter_by(
        usuario_id=usuario_id,
        publicacion_id=publicacion_id
    ).first()

    if guardado_existente:
        db.session.delete(guardado_existente)
        db.session.commit()
        return {
            "success": True,
            "message": "Publicación eliminada de guardados.",
            "guardado": False
        }
    else:
        nuevo_guardado = Guardados(
            usuario_id=usuario_id,
            publicacion_id=publicacion_id
        )
        db.session.add(nuevo_guardado)
        try:
            db.session.commit()
            return {
                "success": True,
                "message": "Publicación guardada exitosamente.",
                "guardado": True
            }
        except IntegrityError:
            db.session.rollback()
            # En este caso significa que ya estaba guardado (race condition o doble click rápido)
            return {
                "success": True,
                "message": "Ya estaba guardada.",
                "guardado": True
            }
        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"Error inesperado: {str(e)}",
                "guardado": False
            }

from sqlalchemy.orm import joinedload

from sqlalchemy.orm import joinedload

def obtener_guardados_service():
    usuario_id = obtener_usuario_id_autenticado()
    if not usuario_id:
        return []

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
