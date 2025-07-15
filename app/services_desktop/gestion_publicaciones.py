from app.models.usuario import Usuario
from flask import request, session
from app.services.jwt_service import generar_token, verificar_token
from app.models.publicaciones import Publicaciones




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
    categoria_id = data.get('categoria_id')

    

    
    if publicacion_id:
        query = query.filter(Publicaciones.publicacion_id==publicacion_id)

    if fecha:
        query  = query.filter(Publicaciones.fecha==fecha)

    if categoria_id:
        query = query.filter(Publicaciones.categoria_id==categoria_id)

    publicaciones = query.all()

    resultado = []
    

    for publicacion in publicaciones:
        resultado.append({
            "publicacion_id": publicacion.publicacion_id,
            "usuario_id": publicacion.usuario_id,
            "fecha": publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S")  if publicacion.fecha else None, 
            "titulo": publicacion.titulo,
            "precio": publicacion.precio,
            "categoria_id": publicacion.categoria_id,
            "tipo_categoria": publicacion.categoria.tipo_categoria,
            "subcategoria_id": publicacion.subcategoria_id,
            "nombre_subcategoria": publicacion.subcategoria.nombre_subcategoria,
            "descripcion_publicacion": publicacion.descripcion_publicacion
        })

    return {"success": True, "lista_publicaciones": resultado}