# app/services_movil/inicio.py (o donde tengas inicio_service)
from app.services_movil.autenticacion import verificar_autenticacion_service
from app.services_movil.configuracion import obtener_datos_usuario_service
from app.services_movil.publi_recientes import (
    obtener_publicaciones_recientes_service,
    obtener_publicaciones_aleatorias_service
)
from flask import session, request

def inicio_service():
    # 1) Obtener token de sesión o header
    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    # 2) Publicaciones siempre se devuelven
    publicaciones_recientes = obtener_publicaciones_recientes_service()
    publicaciones_aleatorias = obtener_publicaciones_aleatorias_service()

    # 3) Inicializar valores
    rol_usuario = None
    primer_nombre = ""
    id_usuario_reportador = None

    # 4) Si hay token, verificar autenticación
    if token:
        auth_result = verificar_autenticacion_service(token)
        if auth_result.get("authenticated"):
            datos_usuario = obtener_datos_usuario_service(token)
            primer_nombre = datos_usuario.get("primer_nombre", "").title()
            id_usuario_reportador = datos_usuario.get("usuario_id")
            rol_usuario = datos_usuario.get("rol_usuario")

    print("📤 Datos que se van a enviar desde inicio_service:", {
        "primer_nombre": primer_nombre,
        "id_usuario_logueado": id_usuario_reportador,
        "rol_usuario": rol_usuario
    })

    return {
        "success": True,
        "primer_nombre": primer_nombre,
        "publicaciones_recientes": publicaciones_recientes,
        "publicaciones_aleatorias": publicaciones_aleatorias,
        "rol_usuario": rol_usuario,
        "id_usuario_logueado": id_usuario_reportador
    }