from app.models.usuario import Usuario
from app.models.reportes import Reportes
from app.models.roles import Roles
from app.models.perfiles import perfiles
from flask import request, session
from app.extensions import db
from app.services.jwt_service import generar_token, verificar_token


# Servicio para gestionar reportes 
def gestion_reportes_admin_service(data):
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
    
    query= Reportes.query

    reporte_id = data.get('reporte_id')
    reportador_id = data.get('reportador_id')
    rol = data.get('tipo_rol')

    # Hace un filtro de los reportes que debe traer

    if reporte_id:
        query = query.filter(Reportes.reporte_id==reporte_id)

    
    if reportador_id:
        query = query.filter(Reportes.reportador_id==reportador_id)
    
    if rol:
        query= query.join(Reportes.reportador).join(Usuario.rol).filter(Roles.tipo_rol==rol)
        query = query.distinct()
    
    reportes = query.all()

    lista_reportes = []

    for reporte in reportes:
        lista_reportes.append({
            "reporte_id": reporte.reporte_id,
            "usuario_id_reportador": reporte.reportador.usuario_id,
            "rol_reportador": reporte.reportador.rol.tipo_rol,
            "descripcion_reporte":reporte.descripcion_reporte,
            "fecha_reporte": reporte.fecha_reporte,
            "reportador_id":reporte.reportador_id,
            "reportado_id":reporte.reportado_id,
            "reportador_nombre": reporte.reportador.perfiles.primer_nombre,
            "reportado_nombre": reporte.asignado.perfiles.primer_nombre
        })
    return {"success": True, "reportes": lista_reportes}






