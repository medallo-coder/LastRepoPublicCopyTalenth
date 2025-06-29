from flask import session, current_app
from app.services.jwt_service import verificar_token
from app.models.usuario import Usuario
from app.models.perfiles import Perfiles
from app.extensions import db
import os
from werkzeug.utils import secure_filename

def obtener_usuario_id():
    token = session.get('jwt')
    if not token:
        return None, "No estás autenticado."

    resultado = verificar_token(token)
    if not resultado["valid"]:
        return None, resultado["message"]

    return resultado["payload"].get("usuario_id"), None


def actualizar_perfil_cliente_service(data, campos=None):
    usuario_id, error = obtener_usuario_id()
    if error:
        return {"success": False, "message": error}

    perfil = Perfiles.query.filter_by(id_usuario=usuario_id).first()
    if not perfil:
        return {"success": False, "message": "Perfil no encontrado."}

    for campo in campos or []:
        if campo in data:
            setattr(perfil, campo, data[campo])

    try:
        db.session.commit()
        return {"success": True, "message": "Perfil actualizado correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al actualizar perfil: {str(e)}"}


def subir_foto_perfil_service(file):
    if not file or file.filename == '':
        return {"success": False, "message": "No se seleccionó ninguna imagen."}

    usuario_id, error = obtener_usuario_id()
    if error:
        return {"success": False, "message": error}

    perfil = Perfiles.query.filter_by(id_usuario=usuario_id).first()
    if not perfil:
        return {"success": False, "message": "Perfil no encontrado."}

    filename = secure_filename(file.filename)
    carpeta = os.path.join(current_app.root_path, 'static/uploads')
    os.makedirs(carpeta, exist_ok=True)
    ruta_archivo = os.path.join(carpeta, filename)
    file.save(ruta_archivo)

    perfil.foto_perfil = filename
    try:
        db.session.commit()
        return {"success": True, "message": "Foto actualizada con éxito."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al guardar foto: {str(e)}"}

def obtener_datos_usuario_service():
    usuario_id, error = obtener_usuario_id()
    if error:
        return {}

    perfil = Perfiles.query.filter_by(id_usuario=usuario_id).first()
    if not perfil:
        return {}

    return {
        "primer_nombre": perfil.primer_nombre,
        "segundo_nombre": perfil.segundo_nombre,
        "primer_apellido": perfil.primer_apellido,
        "segundo_apellido": perfil.segundo_apellido,
        "direccion": perfil.direccion,
        "foto_perfil": perfil.foto_perfil
    }
