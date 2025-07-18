from app.models import Publicaciones, Categorias, Subcategorias
from app import db
from flask import session

# 🔍 Servicio para obtener todas las publicaciones del usuario autenticado
def obtener_mis_publicaciones_service(usuario_id):
    return Publicaciones.query.filter_by(usuario_id=usuario_id).all()


# 🔢 Servicio para obtener el conteo de publicaciones de un usuario
def contar_publicaciones_usuario(usuario_id):
    publicaciones = Publicaciones.query.filter_by(usuario_id=usuario_id).all()
    cantidad_actual = len(publicaciones)
    limite_maximo = 3  # Puedes cambiar este valor según tu lógica

    return {
        "cantidad_actual": cantidad_actual,
        "limite_maximo": limite_maximo
    }


# 💾 Servicio para guardar o actualizar una publicación
# app/services/publicaciones.py
def guardar_mi_publicacion_service(data):
    try:
        usuario_id = data.get('usuario_id')
        publicacion_id = data.get('id')  # vendrá si es edición

        # Validación básica
        titulo = data.get('titulo', '').strip()
        descripcion = data.get('descripcion_publicacion', '').strip()

        if not titulo or not descripcion:
            return {"success": False, "message": "Título y descripción son obligatorios."}

        # Si es edición
        if publicacion_id:
            publicacion = Publicaciones.query.get(int(publicacion_id))

            if not publicacion:
                return {"success": False, "message": "La publicación no existe."}
            if publicacion.usuario_id != usuario_id:
                return {"success": False, "message": "No autorizado."}

            # Actualizar campos
            publicacion.titulo = titulo
            publicacion.descripcion_publicacion = descripcion
            publicacion.id_categoria = data.get("id_categoria")
            publicacion.id_subcategoria = data.get("id_subcategoria")

            db.session.commit()
            return {"success": True, "message": "Publicación actualizada exitosamente."}

        # Si es nueva publicación
        conteo = contar_publicaciones_usuario(usuario_id)
        if conteo["cantidad_actual"] >= conteo["limite_maximo"]:
            return {"success": False, "message": "Límite de publicaciones alcanzado."}

        nueva = Publicaciones(
            titulo=titulo,
            descripcion_publicacion=descripcion,
            id_categoria=data.get("id_categoria"),
            id_subcategoria=data.get("id_subcategoria"),
            usuario_id=usuario_id
        )
        db.session.add(nueva)
        db.session.commit()
        return {"success": True, "message": "Publicación creada correctamente."}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error interno: {str(e)}"}

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
