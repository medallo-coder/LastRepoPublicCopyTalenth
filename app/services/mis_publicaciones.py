from app.models import Publicaciones, Categorias, Subcategorias
from app import db
from flask import session

# 🔍 Servicio para obtener todas las publicaciones del usuario autenticado
def obtener_mis_publicaciones_service(usuario_id):
    return Publicaciones.query.filter_by(usuario_id=usuario_id).all()
# 💾 Servicio para guardar o actualizar una publicación
def guardar_mi_publicacion_service(data):
    try:
        titulo = data.get('titulo')
        descripcion = data.get('descripcion_publicacion')

        if not titulo or not descripcion:
            return {
                "success": False,
                "message": "Título y descripción son obligatorios.",
                "categoria": "error"
            }

        if data.get('publicacion_id'):
            publicacion = Publicaciones.query.get(int(data['publicacion_id']))
            if not publicacion or publicacion.usuario_id != data['usuario_id']:
                return {
                    "success": False,
                    "message": "Publicación no válida o no autorizada.",
                    "categoria": "error"
                }
        else:
            publicacion = Publicaciones(usuario_id=data['usuario_id'])

        publicaciones_usuario = Publicaciones.query.filter_by(usuario_id=data['usuario_id']).all()
        cantidad_no = sum(1 for p in publicaciones_usuario if p.destacada == 'no')
        cantidad_si = sum(1 for p in publicaciones_usuario if p.destacada == 'si')

        if cantidad_si == 1:
            if cantidad_no >= 2:
                return {
                    "success": False,
                    "message": "Ya tienes 1 destacada y 2 normales. Límite de publicaciones alcanzado.",
                    "categoria": "error"
                }
            tipo_destacada = "no"
        elif cantidad_si == 0:
            if cantidad_no >= 2:
                return {
                    "success": False,
                    "message": "Límite alcanzado. Mejora tu visibilidad con una publicación extra y \"destacada\". ¡Activa la promoción ahora y llega a más personas!",
                    "categoria": "error"
                }
            tipo_destacada = "no"
        else:
            return {
                "success": False,
                "message": "Límite de publicaciones alcanzado. Solo se permite 1 destacada y 2 normales.",
                "categoria": "error"
            }

        publicacion.titulo = titulo
        publicacion.precio = data.get('precio') or None
        publicacion.categoria_id = data.get('categoria_id') or None
        publicacion.subcategoria_id = data.get('subcategoria_id') or None
        publicacion.descripcion_publicacion = descripcion
        publicacion.destacada = tipo_destacada

        db.session.add(publicacion)
        db.session.commit()

        return {
            "success": True,
            "message": "Publicación guardada correctamente.",
            "categoria": "success"
        }

    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "categoria": "error"
        }


# 📚 Servicio para obtener todas las categorías
def obtener_categorias_service():
    return Categorias.query.all()

# 📚 Servicio para obtener todas las subcategorías
def obtener_subcategorias_service():
    return Subcategorias.query.all()

# 🔍 Servicio para obtener una publicación por su ID
def obtener_publicacion_por_id_service(publicacion_id):
    return Publicaciones.query.get(publicacion_id)

# 🗑️ Servicio para eliminar una publicación
def eliminar_publicacion_service(publicacion_id):
    try:
        publicacion = Publicaciones.query.get(publicacion_id)
        if not publicacion:
            return {
                "success": False,
                "message": "Publicación no encontrada"
            }
       

        db.session.delete(publicacion)
        db.session.commit()

        return {
            "success": True,
            "message": "Eliminada correctamente"
        }

    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }
