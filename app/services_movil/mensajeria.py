# app/services_movil/mensajeria.py
from app.extensions import db
from app.models.mensajeria import Mensajeria
from app.models.usuario import Usuario
from app.models.calificaciones import Calificaciones
from datetime import datetime, date
from sqlalchemy import or_, and_
from flask import request, session
from app.services_movil.jwt_service import verificar_token


def obtener_mensajes_service(yo_id, otro_id):
    mensajes = (
        db.session.query(Mensajeria)
        .filter(
            or_(
                and_(Mensajeria.id_emisor == yo_id, Mensajeria.id_receptor == otro_id),
                and_(Mensajeria.id_emisor == otro_id, Mensajeria.id_receptor == yo_id),
            )
        )
        .order_by(Mensajeria.fecha.asc())
        .all()
    )
    return [m.to_dict() for m in mensajes]



def enviar_mensaje_service(id_emisor, id_receptor, texto):
    """
    Inserta un nuevo mensaje si el receptor existe.
    """
    # Validar que el receptor exista
    receptor = Usuario.query.get(id_receptor)
    if not receptor:
        return {"success": False, "message": "El receptor no existe"}

    nuevo = Mensajeria(
        id_emisor=id_emisor,
        id_receptor=id_receptor,
        texto=texto,
        fecha=datetime.utcnow(),
        leido=False
    )
    db.session.add(nuevo)
    db.session.commit()
    return {"success": True, "mensaje": nuevo.to_dict()}



def guardar_calificacion_service(data):

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
    
 
    
    calificado_id = data.get('calificado_id')
    reseña = data.get('reseña')
    puntaje = data.get('valor_calificacion')
    
    print(f"💾 DATOS RECIBIDOS:  {calificado_id}, {reseña}, {puntaje}")
    
    # Validar datos
    if  not calificado_id or not reseña or not puntaje:
        return {"success": False, "message": "Todos los campos son obligatorios"}


    # Guardar en la base de datos
    
    nueva_calificacion = Calificaciones(
            reseña=reseña,
            puntaje=puntaje,
            fecha_calificacion=date.today(),
            calificador_id=usuario_id,
            calificado_id=calificado_id
        )
    db.session.add(nueva_calificacion)
    db.session.commit()

    return {"success": True, "message": "Calificación enviada correctamente"}

    
        
