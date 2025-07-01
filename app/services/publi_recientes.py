from app.models.publicaciones import Publicaciones  # Asegúrate de tener el modelo correcto
from app.models.usuario import Usuario  # Asegúrate de tener el modelo correcto


def obtener_publicaciones_recientes_service():
    publicaciones = Publicaciones.query.order_by(Publicaciones.fecha.desc()).limit(10).all()
    return publicaciones

