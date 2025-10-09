# app/services_movil/mensajeria.py
from app.extensions import db
from app.models.mensajeria import Mensajeria
from app.models.usuario import Usuario
from datetime import datetime
from sqlalchemy import or_, and_

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