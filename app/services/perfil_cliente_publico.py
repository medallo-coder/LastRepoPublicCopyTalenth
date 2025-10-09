# app/services/perfil_clientepublico.py
from app.models.perfiles import perfiles  # Modelo del cliente
from app.models.usuario import Usuario
from app.models.calificaciones import Calificaciones  # Asegúrate de tener el modelo correcto
from app import db

def obtener_perfil_clientepublico_service(usuario_id):
    """
    Devuelve la información pública del cliente para mostrar en su perfil público.
    """
    # Traer perfil del cliente
    perfil = perfiles.query.filter_by(id_usuario=usuario_id).first()
    return perfil
