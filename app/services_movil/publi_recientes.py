# app/services_movil/publicaciones.py (ejemplo)
from app.models.publicaciones import Publicaciones
from app import db

def map_to_card(pub):
    return {
        "nombre": pub["nombre"],
        "profesion": pub["profesion"],
        "descripcion": pub["descripcion"],
        "costo": pub["costo"],
        "calificacion": pub["calificacion"]
    }


def obtener_publicaciones_recientes_service(limit=10):
    pubs = db.session.query(Publicaciones).order_by(Publicaciones.fecha.desc()).limit(limit).all()
    return [map_to_card(p.to_dict()) for p in pubs]

def obtener_publicaciones_aleatorias_service(limit=10):
    pubs = db.session.query(Publicaciones).limit(limit).all()
    return [map_to_card(p.to_dict()) for p in pubs]
