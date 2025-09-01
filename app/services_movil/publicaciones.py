#Funcion para publicaciones generales interfaz
from datetime import datetime, timedelta 
from app.models.categorias import Categorias
from app.models.publicaciones import Publicaciones



def guardar_publicacion_usuario_service(data):
    categoria_id = data.get('categoria_id')
    subcategoria_id = data.get('subcategoria_id')
    tiempo = data.get('tiempo')  # Puede ser '24h', 'semana', 'mes', etc.

    # Obtener todas las categorías para los filtros
    categorias = Categorias.query.all()

    # Base query
    publicaciones_query = Publicaciones.query

    if categoria_id:
        publicaciones_query = publicaciones_query.filter_by(categoria_id=categoria_id)

    if subcategoria_id:
        publicaciones_query = publicaciones_query.filter_by(subcategoria_id=subcategoria_id)

    # Filtro por tiempo
    if tiempo == "24h":
        desde = datetime.now() - timedelta(hours=24)
        publicaciones_query = publicaciones_query.filter(Publicaciones.fecha >= desde)
    elif tiempo == "semana":
        desde = datetime.now() - timedelta(days=7)
        publicaciones_query = publicaciones_query.filter(Publicaciones.fecha >= desde)
    elif tiempo == "mes":
        desde = datetime.now() - timedelta(days=30)
        publicaciones_query = publicaciones_query.filter(Publicaciones.fecha >= desde)
    # Si no hay filtro, no aplicamos nada

    # Ordenar de más reciente a más antigua
    publicaciones = publicaciones_query.order_by(Publicaciones.fecha.desc()).all()

    return{"success":True,
            "publicaciones_generales":[p.to_dict() for p in publicaciones],
            "categorias":[c.to_dict() for c in categorias],
              "total_resultados": len(publicaciones),
              "categoria_selecionada": categoria_id}

  
    