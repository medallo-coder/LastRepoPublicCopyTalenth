from app.models import Publicaciones, Categorias, Subcategorias
from app import db
from flask import session
from sqlalchemy import or_
# 🔍 Servicio para obtener todas las publicaciones del usuario autenticado
def obtener_mis_publicaciones_service(usuario_id):
    return Publicaciones.query.filter_by(usuario_id=usuario_id).all()

# 🔢 Servicio para obtener el conteo de publicaciones de un usuario
def contar_publicaciones_usuario(usuario_id):
    publicaciones = Publicaciones.query.filter_by(usuario_id=usuario_id).all()
    
    # ✅ Contar solo publicaciones completas
    cantidad_completas = sum(1 for pub in publicaciones if pub.titulo and pub.descripcion_publicacion)

    # ✅ Contar slots vacíos (pagados pero sin datos aún)
    slots_vacios = sum(1 for pub in publicaciones if not pub.titulo or not pub.descripcion_publicacion)

    limite_maximo = 2  # o tu lógica de negocio

    return {
        "cantidad_actual": cantidad_completas,
        "limite_maximo": limite_maximo,
        "slots_vacios": slots_vacios
    }

# 💾 Servicio para guardar o actualizar una publicación
def guardar_mi_publicacion_service(data):
    try:
        usuario_id = data.get('usuario_id')
        publicacion_id = data.get('id')
        # Validación básica
        titulo = data.get('titulo', '').strip()
        descripcion = data.get('descripcion_publicacion', '').strip()
        precio = data.get('precio')
        destacada = data.get("destacada")

        
        print(f"ID DE LA PUBLICACION: {publicacion_id}")  # vendrá si es edición
        print(f"TITULO DE LA PUBLICACION: {titulo}")  # vendrá si es edición
        print(f"DESCRIPCION DE LA PUBLICACION: {descripcion}")  # vendrá si es edición
        print(f"DESTACADA:  {destacada}")

        
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

        

        # 1️⃣ Si es edición
        if publicacion_id:
            publicacion = Publicaciones.query.get(int(publicacion_id))
            if not publicacion:
                return {"success": False, "message": "La publicación no existe."}
            if publicacion.usuario_id != usuario_id:
                return {"success": False, "message": "No autorizado."}
            
             # 🔹 Validar reglas de negocio al editar
            if destacada == "si":
                # Ver si ya existe otra publicación destacada del mismo usuario
                otra_destacada = Publicaciones.query.filter(
                    Publicaciones.usuario_id == usuario_id,
                    Publicaciones.publicacion_id != publicacion.publicacion_id,
                    Publicaciones.destacada == "si"
                ).first()

                if otra_destacada:
                    return {"success": False, "message": "Ya tienes otra publicación destacada activa."}

            if destacada == "no":
                # Ver cuántas normales tiene (excluyendo la actual)
                otras_normales = Publicaciones.query.filter(
                    Publicaciones.usuario_id == usuario_id,
                    Publicaciones.publicacion_id != publicacion.publicacion_id,
                    Publicaciones.destacada == "no",
                    Publicaciones.titulo.isnot(None),
                    Publicaciones.descripcion_publicacion.isnot(None)
                ).count()

                if otras_normales >= 1:
                    return {"success": False, "message": "Solo puedes tener una publicación normal además de la destacada."}

            # ✅ Si pasa las validaciones, actualizar
            publicacion.titulo = titulo
            publicacion.descripcion_publicacion = descripcion
            publicacion.precio = precio
            publicacion.categoria_id = data.get("categoria_id")
            publicacion.subcategoria_id = data.get("subcategoria_id")
            publicacion.destacada = destacada


            db.session.commit()
            return {"success": True, "message": "Publicación actualizada exitosamente."}
        
        publicaciones_usuario = Publicaciones.query.filter_by(usuario_id=usuario_id).all()
        print(f"📝 Todas las publicaciones del usuario {usuario_id}:")
        for pub in publicaciones_usuario:
            print({
        "id": pub.publicacion_id,
        "usuario_id": pub.usuario_id,
        "titulo": pub.titulo,
        "descripcion": pub.descripcion_publicacion,
        "destacada": pub.destacada,
        "estado": pub.estado
    })



        # 2️⃣ Si existe un slot vacío (pagado por Mercado Pago)
        slot = Publicaciones.query.filter(
        Publicaciones.usuario_id == usuario_id,
        or_(
            Publicaciones.titulo.is_(None),
            Publicaciones.titulo == "",
            Publicaciones.descripcion_publicacion.is_(None),
            Publicaciones.descripcion_publicacion == ""
        )
).first()

        
        print("🔍 DEBUG SLOT VACÍO ->", slot)   # 👈 Para ver si encontró algo en consola
        
        
        if slot:

            print("🟢 SLOT DETECTADO ->", {
                "id": slot.publicacion_id,
                "usuario_id": slot.usuario_id,
                "titulo": slot.titulo,
                "descripcion": slot.descripcion_publicacion,
                "destacada": slot.destacada,
                "estado": slot.estado
            })  # 👈 Muestra datos antes de actualizarlos

            slot.titulo = titulo
            slot.descripcion_publicacion = descripcion
            slot.precio = precio
            slot.categoria_id = data.get("categoria_id")
            slot.subcategoria_id = data.get("subcategoria_id")
            slot.destacada = "si"
            slot.estado = "activo"
            db.session.commit()
            return {"success": True, "message": "Tu publicación de pago fue creada 🚀"}

        # 3️⃣ Validaciones para nueva publicación gratuita
        publicaciones_usuario = Publicaciones.query.filter(
            Publicaciones.usuario_id == usuario_id,
            Publicaciones.titulo.isnot(None),
            Publicaciones.descripcion_publicacion.isnot(None)
        ).all()

        cantidad_total = len(publicaciones_usuario)
        if cantidad_total >= 2:
            return {"success": False, "message": "Solo se permiten máximo 2 publicaciones por usuario."}

        cantidad_destacadas = sum(1 for pub in publicaciones_usuario if pub.destacada == "si")
        cantidad_normales = cantidad_total - cantidad_destacadas

        if destacada == "si" and cantidad_destacadas >= 1:
            return {"success": False, "message": "Solo puedes tener una publicación destacada."}

        if destacada == "no" and cantidad_normales >= 1:
            return {"success": False, "message": "Solo puedes tener una publicación normal además de la destacada."}

        nueva = Publicaciones(
            titulo=titulo,
            descripcion_publicacion=descripcion,
            precio=precio,
            categoria_id=data.get("categoria_id"),
            subcategoria_id=data.get("subcategoria_id"),
            usuario_id=usuario_id,
            destacada=destacada,
            estado="activo"
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
