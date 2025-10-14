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

def obtener_conversaciones_service(usuario_id):
    """
    Devuelve las conversaciones del usuario con:
    - id del otro usuario
    - nombre y foto del otro usuario
    - último mensaje
    - fecha del último mensaje
    """
    subconsulta = (
        db.session.query(
            db.func.max(Mensajeria.mensaje_id).label("ultimo_id")
        )
        .filter(
            or_(
                Mensajeria.id_emisor == usuario_id,
                Mensajeria.id_receptor == usuario_id,
            )
        )
        .group_by(
            db.case(
                (
                    Mensajeria.id_emisor == usuario_id,
                    Mensajeria.id_receptor,
                ),
                else_=Mensajeria.id_emisor,
            )
        )
        .subquery()
    )

    ultimos_mensajes = (
        db.session.query(Mensajeria)
        .filter(Mensajeria.mensaje_id.in_(subconsulta))
        .order_by(Mensajeria.fecha.desc())
        .all()
    )

    conversaciones = []
    for mensaje in ultimos_mensajes:
        # Determinar quién es el otro usuario
        if mensaje.id_emisor == usuario_id:
            otro = Usuario.query.get(mensaje.id_receptor)
        else:
            otro = Usuario.query.get(mensaje.id_emisor)

        conversaciones.append({
    "usuario_id": otro.usuario_id if otro else None,
    "nombre": (
        f"{otro.perfiles.primer_nombre} {otro.perfiles.primer_apellido}"
        if otro and otro.perfiles else "Usuario desconocido"
    ),
    "foto": (
        otro.perfiles.foto_perfil
        if otro and otro.perfiles and otro.perfiles.foto_perfil else None
    ),
    "ultimo_mensaje": mensaje.texto,
    "fecha": mensaje.fecha.strftime("%Y-%m-%d %H:%M:%S"),
    "visto": mensaje.leido
    })

    return conversaciones



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

    
        
