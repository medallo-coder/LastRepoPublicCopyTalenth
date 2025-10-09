from datetime import date
from app.extensions import db
from app.models.reportes import Reportes
from flask import session, request
from app.services_movil.jwt_service import verificar_token
from app.models.usuario import Usuario


def guardar_reporte_service(data):

    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return {"success": False, "message": "Token no enviado."}

    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario = Usuario.query.filter_by(usuario_id=usuario_id).first()

    if not usuario:
        return{"success": False, "message": "Usuario no encontrado"}
    

    reportador_id = usuario_id
    reportado_id = data.get('reportado_id')
    descripcion = data.get('descripcion')

    print(f"DATOS: {reportado_id}, {reportador_id}, {descripcion}")

    if not reportado_id  or not descripcion:
            return {"success": False, "message":"Faltan datos en el reporte"}
            

    nuevo_reporte = Reportes(
            descripcion_reporte=descripcion,
            fecha_reporte=date.today(),
            reportador_id=reportador_id,
            reportado_id=reportado_id
        )

    db.session.add(nuevo_reporte)
    db.session.commit()
    return {"success":True, "message": "Reporte enviado correctamente"}  
    

   
