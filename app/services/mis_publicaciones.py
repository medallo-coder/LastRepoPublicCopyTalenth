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
                "message": "Título y descripción son obligatorios"
            }

        usuario_id = data['usuario_id']
        destacada = data.get('destacada') in ['true', 'True', '1', True]

        # Contar publicaciones por tipo
        publicaciones_gratis = Publicaciones.query.filter_by(
            usuario_id=usuario_id,
            destacada=False
        ).count()

        publicaciones_destacadas = Publicaciones.query.filter_by(
            usuario_id=usuario_id,
            destacada=True
        ).count()

        total = publicaciones_gratis + publicaciones_destacadas

        if data.get('publicacion_id'):
            publicacion = Publicaciones.query.get(int(data['publicacion_id']))
            if not publicacion or publicacion.usuario_id != usuario_id:
                return {
                    "success": False,
                    "message": "Publicación no válida o no autorizada"
                }

        else:
            if publicaciones_gratis >= 2 and not destacada:
                return {
                    "success": False,
                    "message": "Solo puedes tener 2 publicaciones gratuitas. Destaca tu publicación para añadir otra."
                }

            if publicaciones_destacadas >= 1 and destacada:
                return {
                    "success": False,
                    "message": "Ya tienes una publicación destacada. Elimina una si deseas agregar otra."
                }

            if publicaciones_gratis + publicaciones_destacadas >= 3:
                return {
                    "success": False,
                    "message": "Solo puedes tener un máximo de 3 publicaciones entre gratuitas y destacadas."
                }

            publicacion = Publicaciones(usuario_id=usuario_id)


        # Asignar campos
        publicacion.titulo = titulo
        publicacion.precio = data.get('precio') or None
        publicacion.categoria_id = data.get('categoria_id') or None
        publicacion.subcategoria_id = data.get('subcategoria_id') or None
        publicacion.descripcion_publicacion = descripcion
        publicacion.destacada = destacada

        db.session.add(publicacion)
        db.session.commit()

        return {
            "success": True,
            "message": "Publicación guardada correctamente"
        }

    except Exception:
        db.session.rollback()
        return {
            "success": False,
            "message": "Ocurrió un error inesperado al guardar la publicación."
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
