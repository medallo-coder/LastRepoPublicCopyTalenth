from app.models import Publicaciones, Categorias, Subcategorias
from app import db
from flask import session



def obtener_mis_publicaciones_service(usuario_id):
    return Publicaciones.query.filter_by(usuario_id=usuario_id).all()


def guardar_mi_publicacion_service(data):
    try:
        if data.get('publicacion_id'):
            publicacion = Publicaciones.query.get(int(data['publicacion_id']))
            if not publicacion or publicacion.usuario_id != data['usuario_id']:
                return {"success": False, "message": "Publicación no válida o no autorizada"}
        else:
            publicacion = Publicaciones(usuario_id=data['usuario_id'])

        publicacion.titulo = data['titulo']
        publicacion.precio = data.get('precio') or None
        publicacion.categoria_id = data.get('categoria_id') or None
        publicacion.subcategoria_id = data.get('subcategoria_id') or None
        publicacion.descripcion_publicacion = data.get('descripcion_publicacion')

        db.session.add(publicacion)
        db.session.commit()
        return {"success": True, "message": "Guardado correctamente"}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error: {str(e)}"}
    
    
def obtener_categorias_service():
    return Categorias.query.all()

def obtener_subcategorias_service():
    return Subcategorias.query.all()

def obtener_publicacion_por_id_service(publicacion_id):
    return Publicaciones.query.get(publicacion_id)

def guardar_publicacion_service(data):
    try:
        if data.get('publicacion_id'):
            publicacion = Publicaciones.query.get(int(data['publicacion_id']))
            if not publicacion:
                return {"success": False, "message": "Publicación no encontrada"}
        else:
            publicacion = Publicaciones(usuario_id=session['usuario_id'])

        publicacion.titulo = data['titulo']
        publicacion.precio = data.get('precio') or None
        publicacion.categoria_id = data.get('categoria_id') or None
        publicacion.subcategoria_id = data.get('subcategoria_id') or None
        publicacion.descripcion_publicacion = data.get('descripcion_publicacion')

        db.session.add(publicacion)
        db.session.commit()
        return {"success": True, "message": "Guardado correctamente"}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error: {str(e)}"}

def eliminar_publicacion_service(publicacion_id):
    try:
        publicacion = Publicaciones.query.get(publicacion_id)
        if not publicacion:
            return {"success": False, "message": "Publicación no encontrada"}
        db.session.delete(publicacion)
        db.session.commit()
        return {"success": True, "message": "Eliminada correctamente"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error: {str(e)}"}
