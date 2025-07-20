from app.models.publicaciones import Publicaciones  # Asegúrate de tener el modelo correcto
from app.models.usuario import Usuario  # Asegúrate de tener el modelo correcto
from sqlalchemy import func



def obtener_publicaciones_generales_service():
    return Publicaciones.query.order_by(Publicaciones.fecha.desc()).limit(10).all()


def obtener_publicaciones_filtradas_service(categoria_id=None):
    query = Publicaciones.query

    if categoria_id:
        query = query.filter(Publicaciones.categoria_id == categoria_id)

    publicaciones = query.order_by(Publicaciones.fecha.desc()).all()
    total = query.count()

    return {
        "publicaciones": publicaciones,
        "total_resultados": total
    }

def obtener_publicaciones_filtradas_service(categoria_id=None, subcategoria_id=None):
    query = Publicaciones.query

    if subcategoria_id:
        query = query.filter(Publicaciones.subcategoria_id == subcategoria_id)
    elif categoria_id:
        query = query.filter(Publicaciones.categoria_id == categoria_id)

    publicaciones = query.order_by(Publicaciones.fecha.desc()).all()
    total = query.count()

    return {
        "publicaciones": publicaciones,
        "total_resultados": total
    }
