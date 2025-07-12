from app.models.perfiles import perfiles  # Asegúrate de tener el modelo correcto
from app.models.usuario import Usuario  # Asegúrate de tener el modelo correcto
from sqlalchemy import func


def obtener_perfil_publico_service(usuario_id):
    # 👇 Corrección: usar 'id_usuario' en lugar de 'usuario_id'
    return perfiles.query.filter_by(id_usuario=usuario_id).first()
