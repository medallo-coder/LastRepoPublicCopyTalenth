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
    limite_maximo = 2  # Puedes cambiar este valor según tu lógica

    return {
        "cantidad_actual": cantidad_actual,
        "limite_maximo": limite_maximo
    }

# 💾 Servicio para guardar o actualizar una publicación
def guardar_mi_publicacion_service(data):
    try:
        usuario_id = data.get('usuario_id')
        publicacion_id = data.get('id')  # vendrá si es edición

        # Validación básica
        titulo = data.get('titulo', '').strip()
        descripcion = data.get('descripcion_publicacion', '').strip()
        precio = data.get('precio')  # <- NUEVO

        if not titulo or not descripcion:
            return {"success": False, "message": "Título y descripción son obligatorios."}

        if precio is None or str(precio).strip() == "":
            return {"success": False, "message": "El precio es obligatorio."}

        try:
            precio = float(precio)
            if precio < 0:
                return {"success": False, "message": "El precio no puede ser negativo."}
        except ValueError:
            return {"success": False, "message": "Precio inválido."}

        destacada = data.get("destacada", "no")

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
            publicacion.precio = precio  # <- NUEVO
            publicacion.categoria_id = data.get("categoria_id")
            publicacion.subcategoria_id = data.get("subcategoria_id")
            publicacion.destacada = destacada

            db.session.commit()
            return {"success": True, "message": "Publicación actualizada exitosamente."}

        # Validaciones para nueva publicación
        publicaciones_usuario = Publicaciones.query.filter_by(usuario_id=usuario_id).all()
        cantidad_total = len(publicaciones_usuario)

        if cantidad_total >= 2:
            return {"success": False, "message": "Solo se permiten máximo 2 publicaciones por usuario."}

        cantidad_destacadas = sum(1 for pub in publicaciones_usuario if pub.destacada == "si")
        cantidad_no_destacadas = cantidad_total - cantidad_destacadas

        if destacada == "si" and cantidad_destacadas >= 1:
            return {"success": False, "message": "Solo puedes tener una publicación destacada."}

        if destacada == "no" and cantidad_no_destacadas >= 1 and cantidad_destacadas == 0:
            return {
                "success": False,
                "message": "Debes tener al menos una publicación destacada para poder agregar otra publicación normal."
            }

        # Crear nueva publicación
        nueva = Publicaciones(
            titulo=titulo,
            descripcion_publicacion=descripcion,
            precio=precio,  # <- NUEVO
            categoria_id=data.get("categoria_id"),
            subcategoria_id=data.get("subcategoria_id"),
            usuario_id=usuario_id,
            destacada=destacada
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

# 🔍 Servicio para obtener subcategorías filtradas por categoría
def obtener_subcategorias_por_categoria_service(categoria_id):
    return Subcategorias.query.filter_by(categoria_id=categoria_id).all()
