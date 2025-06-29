from app.extensions import db
from app.models.publicaciones import Publicaciones
from app.models.perfiles import Perfiles 
from app.services.jwt_service import verificar_token
from flask import session


def crear_publicacion_service(data):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "Usuario no autenticado."}

    result = verificar_token(token)
    if not result["valid"]:
        return {"success": False, "message": result["message"]}

    usuario_id = result["payload"].get("usuario_id")

    try:
        # 👉 Buscar perfil del usuario
        perfil = Perfiles.query.filter_by(id_usuario=usuario_id).first()
        nombre_usuario = "Usuario"
        if perfil:
            nombre_usuario = f"{perfil.primer_nombre} {perfil.primer_apellido}"

        # 👉 Verificar si ya tiene 3 publicaciones
        publicaciones_actuales = Publicaciones.query.filter_by(usuario_id=usuario_id).count()
        if publicaciones_actuales >= 3:
            return {
                "success": False,
                "message": "Solo puedes tener 3 publicaciones activas. Elimina una para agregar otra."
            }

        # 👉 Crear publicación
        nueva = Publicaciones(
            usuario_id=usuario_id,
            titulo=data.get("titulo"),  # nota: cambiaste de 'nombre' a 'titulo'
            categoria_id=int(data.get("categoria")),
            subcategoria_id=int(data.get("subcategoria")),
            precio=data.get("precio"),
            descripcion_publicacion=data.get("descripcion")
        )

        db.session.add(nueva)
        db.session.commit()

        # 👉 Responder con los datos necesarios para mostrar la tarjeta
        return {
            "success": True,
            "message": "Publicación creada con éxito.",
            "data": {
                "publicacion_id": nueva.publicacion_id,
                "nombre_usuario": nombre_usuario,
                "titulo": nueva.titulo,
                "precio": nueva.precio,
                "descripcion": nueva.descripcion_publicacion,
                "foto": perfil.foto_perfil if perfil else "default.png",
                "categoria": nueva.categoria_id,
                "subcategoria": nueva.subcategoria_id  
            }
        }

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": str(e)}
    
def editar_publicacion_service(publicacion_id, usuario_id, data):
    try:
        publicacion = Publicaciones.query.filter_by(publicacion_id=publicacion_id, usuario_id=usuario_id).first()

        if not publicacion:
            return {"success": False, "message": "Publicación no encontrada o no autorizada."}

        # Actualizar campos permitidos
        publicacion.titulo = data.get("titulo", publicacion.titulo)
        publicacion.precio = data.get("precio", publicacion.precio)
        publicacion.descripcion_publicacion = data.get("descripcion", publicacion.descripcion_publicacion)
        publicacion.categoria_id = int(data.get("categoria", publicacion.categoria_id))
        publicacion.subcategoria_id = int(data.get("subcategoria", publicacion.subcategoria_id))

        db.session.commit()

        return {
            "success": True,
            "message": "Publicación actualizada exitosamente.",
            "data": {
                "publicacion_id": publicacion.publicacion_id,
                "titulo": publicacion.titulo,
                "precio": publicacion.precio,
                "descripcion": publicacion.descripcion_publicacion,
                "categoria": publicacion.categoria_id,
                "subcategoria": publicacion.subcategoria_id
            }
        }

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al editar publicación: {str(e)}"}

    
def eliminar_publicacion_service(publicacion_id, usuario_id):
    try:
        # Solo eliminar si la publicación pertenece al usuario autenticado
        publicacion = Publicaciones.query.filter_by(publicacion_id=publicacion_id, usuario_id=usuario_id).first()
        
        if not publicacion:
            return {"success": False, "message": "Publicación no encontrada o no autorizada."}
        
        db.session.delete(publicacion)
        db.session.commit()
        return {"success": True, "message": "Publicación eliminada exitosamente."}
    
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al eliminar publicación: {str(e)}"}