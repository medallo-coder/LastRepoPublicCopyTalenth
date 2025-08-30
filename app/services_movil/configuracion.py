from app.services.jwt_service import verificar_token
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.usuario import Usuario
from app.models.perfiles import perfiles
from app.models.idiomas import Idiomas
from app.models.aptitudes import Aptitudes
from app.models.estudios import Estudios
from app.models.experiencias import Experiencias
from app.extensions import db
from app.services.jwt_service import generar_token,generar_token_recuperacion 
from app.services.notificaciones import enviar_link_recuperacion_correo

# Servicio para obtener el nombre, rol y fecha de registro del usuario autenticado
def obtener_datos_usuario_service(token):
    if not token:
        return {
            "primer_nombre": "Invitado", "segundo_nombre": "Invitado", "primer_apellido": "Invitado", "segundo_apellido": "Invitado", "direccion": "Invitado", "": "Invitado", "rol": "Invitado", "fecha_registro": "N/A", "correo": "Invitado",  "nombre_idioma": "N/A"  } 

    resultado = verificar_token(token)
    if not resultado.get("valid"):
        return {"primer_nombre": "Invitado", "segundo_nombre": "Invitado", "primer_apellido": "Invitado", "segundo_apellido": "Invitado", "direccion": "Invitado", "": "Invitado", "rol": "Invitado", "fecha_registro": "N/A", "correo": "Invitado", "nombre_idioma": "N/A"  }

    payload = resultado.get("payload")
    usuario_id = payload.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return {"primer_nombre": "Invitado", "segundo_nombre": "Invitado", "primer_apellido": "Invitado", "segundo_apellido": "Invitado", "direccion": "Invitado", "": "Invitado", "rol": "Invitado", "fecha_registro": "N/A", "correo": "Invitado", "nombre_idioma": "N/A"  }
    
    # Obtener la fecha de registro y formatearla
    fecha_registro = usuario.fecha_registro
    fecha_formateada = fecha_registro.strftime("%B de %Y")  # Ejemplo: Noviembre de 2020

    

    usuario=Usuario.query.get(usuario_id)
    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()
    aptitudes=Aptitudes.query.filter_by(id_perfil= perfil.id_perfil).first()
    estudios=Estudios.query.filter_by(id_perfil= perfil.id_perfil).first()
    experiencias=Experiencias.query.filter_by(id_perfil=perfil.id_perfil).first()

    nombre_idioma = ", ".join([idioma.nombre_idioma for idioma in perfil.idioma]) if perfil.idioma else ""
 
    return {
        "usuario_id": usuario.usuario_id,
        "id_perfil": perfil.id_perfil,
        "primer_nombre": perfil.primer_nombre,
        "segundo_nombre": perfil.segundo_nombre,
        "primer_apellido": perfil.primer_apellido,
        "segundo_apellido": perfil.segundo_apellido,
        "direccion": perfil.direccion,
        "correo": usuario.correo,
        "descripcion_perfil": perfil.descripcion_perfil,
        "rol": usuario.rol.tipo_rol,
        "nombre_idioma": nombre_idioma,
        "tipo_aptitud": aptitudes.tipo_aptitud if aptitudes else None,
        "institucion": estudios.institucion if estudios else None ,
        "titulo_obtenido": estudios.titulo_obtenido if estudios else None ,
        "fecha_inicio": estudios.fecha_inicio if estudios else None ,
        "fecha_fin": estudios.fecha_fin if estudios else None ,
        "nombre": experiencias.nombre if experiencias else None ,
        "descripcion": experiencias.descripcion if experiencias else None ,
        "fecha_inicio_experiencia": experiencias.fecha_inicio_experiencia if experiencias else None ,
        "fecha_fin_experiencia": experiencias.fecha_fin_experiencia if experiencias else None ,
        "foto_perfil": perfil.foto_perfil if perfil else None,

        "fecha_registro": f"Se unió en {fecha_formateada}"  # Formateamos la fecha
    }
