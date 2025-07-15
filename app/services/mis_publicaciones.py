from app.models import Publicaciones, Categorias, Subcategorias
from app import db
from flask import session

# 🔍 Servicio para obtener todas las publicaciones del usuario autenticado
def obtener_mis_publicaciones_service(usuario_id):
    return Publicaciones.query.filter_by(usuario_id=usuario_id).all()

# 💾 Servicio para guardar o actualizar una publicación
def guardar_mi_publicacion_service(data):
    try:
        # Validar campos obligatorios antes de crear o actualizar
        titulo = data.get('titulo')
        descripcion = data.get('descripcion_publicacion')

        if not titulo or not descripcion:
            return {
                "success": False,
                "message": "Título y descripción son obligatorios"
            }

        # Si viene un ID, es una edición
        if data.get('publicacion_id'):
            publicacion = Publicaciones.query.get(int(data['publicacion_id']))
            if not publicacion or publicacion.usuario_id != data['usuario_id']:
                return {
                    "success": False,
                    "message": "Publicación no válida o no autorizada"
                }
        else:
            # Crear nueva publicación solo si los datos son válidos
            publicacion = Publicaciones(usuario_id=data['usuario_id'], cantidad=0)


        tipo_destacada =  "gratis"


        cantidad_actual = Publicaciones.query.filter_by(usuario_id=data['usuario_id']).count()
        cantidad_gratis= Publicaciones.query.filter_by(usuario_id=data['usuario_id'], destacada='gratis').count()
        cantidad_destacada= Publicaciones.query.filter_by(usuario_id=data['usuario_id'], destacada='destacada').count()

        

        if cantidad_gratis + cantidad_destacada >=3:
            return{
                "success": False, "message": "Maximo de publicaciones son 3"
            }

        if tipo_destacada == "gratis" and cantidad_gratis >= 2 :
            return{
                "success": False, "message": "Solo puedes tener 2 publicaciones gratuitas. Paga para mas."
            }
        
        
        if tipo_destacada == "destacada" and cantidad_destacada >=1 :
            return{
                "success": False, "message": "Solo puedes tener tres publicaciones 1 destacada y 2 gratis"
            }
            

        # Asignar campos
        publicacion.titulo = titulo
        publicacion.precio = data.get('precio') or None
        publicacion.categoria_id = data.get('categoria_id') or None
        publicacion.subcategoria_id = data.get('subcategoria_id') or None
        publicacion.descripcion_publicacion = descripcion
        publicacion.cantidad = cantidad_actual + 1
        publicacion.destacada = tipo_destacada


            # Guardar en la base de datos
        db.session.add(publicacion)
        db.session.commit()

        return {
            "success": True,
            "message": "Guardado correctamente"
            }

    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "message": f"Error: {str(e)}"
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
