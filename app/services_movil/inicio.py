from app.services_movil.autenticacion import verificar_autenticacion_service
from app.services_movil.configuracion import obtener_datos_usuario_service
from app.services_movil.rol_service import verificar_rol
from app.services_movil.publi_recientes import obtener_publicaciones_recientes_service, obtener_publicaciones_aleatorias_service
from flask import session, request

def inicio_service():
    # Obtener token de la sesión y verificar
    # Si no hay token en sesión, intenta obtenerlo del header Authorization
    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        return {"success": True, "message": "Token no enviado"}

    publicaciones_recientes = obtener_publicaciones_recientes_service()
    publicaciones_aleatorias = obtener_publicaciones_aleatorias_service()
    rol_usuario = verificar_rol(token)  # Verifica el rol del usuario autenticado
    primer_nombre = ""
    id_usuario_reportador = None
    
    auth_result = verificar_autenticacion_service(token)

    if auth_result.get("authenticated"):
        datos_usuario = obtener_datos_usuario_service(token)
        primer_nombre = datos_usuario.get("primer_nombre", "").title()
        usuario_id = obtener_datos_usuario_service(token)
        id_usuario_reportador = usuario_id.get("usuario_id")
        

    return{
        "success": True,
        "primer_nombre":primer_nombre,
        "publicaciones_recientes":publicaciones_recientes,
        "publicaciones_aleatorias":publicaciones_aleatorias,
        "rol_usuario":rol_usuario,
        "id_usuario_logueado":id_usuario_reportador
        }
        
        
    