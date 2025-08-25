from app.models.usuario import Usuario
from app.models.publicaciones import Publicaciones
from flask import request, session
from app.extensions import db
from app.services.jwt_service import generar_token, verificar_token
from app.models.publicaciones import Publicaciones
from app.models.categorias import Categorias



# Servicio para gestionar publicaciones
def gestion_publicaciones_admin_service(data):
    token = session.get('jwt')

      # Si no hay token en sesión, intenta obtenerlo del header Authorization
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return {"success": True, "message": "Token no enviado"}
    
    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario_admin = Usuario.query.filter_by(usuario_id=usuario_id).first()
    
    if not usuario_admin:
        return{"success": False, "message": "Usuario no encontrado"}
    
    if usuario_admin.id_rol != 3:
        return{"success": False, "message": "No tienes permisos de administrador"}
    
    query= Publicaciones.query

    publicacion_id = data.get('publicacion_id')
    fecha = data.get('fecha')
    tipo_categoria = data.get('tipo_categoria')

    
    # Hace un filtro de las publicaciones que debe de traer
    
    if publicacion_id:
        query = query.filter(Publicaciones.publicacion_id==publicacion_id)

    if fecha:
        query  = query.filter(Publicaciones.fecha==fecha)

    if  tipo_categoria:
        query = query.join(Publicaciones.categoria).filter(Categorias.tipo_categoria == tipo_categoria)


    # Trae las publicaciones que se asignaron con ese filtro
    publicaciones = query.all()

    # Se guardan las publicaciones en el array resultado
    resultado = []
    

    for publicacion in publicaciones:
        perfil = publicacion.usuario.perfiles
        resultado.append({
            "publicacion_id": publicacion.publicacion_id,
            "usuario_id": publicacion.usuario_id,
            "fecha": publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S")  if publicacion.fecha else None, 
            "titulo": publicacion.titulo,
            "precio": publicacion.precio,
            "categoria_id": publicacion.categoria_id,
            "categorias": publicacion.categoria.tipo_categoria,
            "subcategoria_id": publicacion.subcategoria_id,
            "nombre_subcategoria": publicacion.subcategoria.nombre_subcategoria,
            "descripcion_publicacion": publicacion.descripcion_publicacion,
            "primer_nombre": perfil.primer_nombre if perfil else "" ,
            "primer_apellido": perfil.primer_apellido if perfil else ""
        })

    return {"success": True, "lista_publicaciones": resultado}

# Servicio para eliminar publicaciones 
def eliminar_publicaciones_admin_service(data):
    token = session.get('jwt')

      # Si no hay token en sesión, intenta obtenerlo del header Authorization
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return {"success": True, "message": "Token no enviado"}
    
    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario_admin = Usuario.query.filter_by(usuario_id=usuario_id).first()
    
    if not usuario_admin:
        return{"success": False, "message": "Usuario no encontrado"}
    
    if usuario_admin.id_rol != 3:
        return{"success": False, "message": "No tienes permisos de administrador"}
    
    publicacion_id = data.get('publicacion_id')

    publicaciones = Publicaciones.query.get(publicacion_id)

    # Verificamos si la publicacion no existe
    if not publicaciones:
        return {"success": False, "message": f"La publicacion con el id {publicacion_id}, no existe"}
    
    # Si existe se elimina
    db.session.delete(publicaciones)
    db.session.commit()

    return {"success": True, "message": f"La publicacion con el ID {publicacion_id}, fue eliminada"}