from app.models.publicaciones import Publicaciones  # Asegúrate de tener el modelo correcto
from app.models.usuario import Usuario  # Asegúrate de tener el modelo correcto
from sqlalchemy import func



def obtener_publicaciones_recientes_service():
    return Publicaciones.query.filter_by(estado="activo").filter_by(destacada="no").order_by(Publicaciones.fecha.desc()).limit(10).all()
def obtener_publicaciones_aleatorias_service():
    return Publicaciones.query.filter_by(estado="activo").filter_by(destacada="si").order_by(Publicaciones.fecha.desc()).limit(10).all()
    
