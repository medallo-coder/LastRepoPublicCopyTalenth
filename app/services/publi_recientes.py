from app.models.publicaciones import Publicaciones  # Asegúrate de tener el modelo correcto
from app.models.usuario import Usuario  # Asegúrate de tener el modelo correcto
from sqlalchemy import func



def obtener_publicaciones_recientes_service():
    return Publicaciones.query.order_by(Publicaciones.fecha.desc()).limit(10).all()

def obtener_publicaciones_aleatorias_service():
    return Publicaciones.query.order_by(func.random()).all()
