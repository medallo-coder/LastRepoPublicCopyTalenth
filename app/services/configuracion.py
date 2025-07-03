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
# Servicio para cambiar la contraseña
def cambiar_contrasena_service(data):
    actual_contrasena = data.get("actual_contrasena")
    nueva_contrasena = data.get("nueva_contrasena")
    confirmar_contrasena = data.get("confirmar_contrasena")

    # Verificar que todos los campos estén presentes
    if not actual_contrasena or not nueva_contrasena or not confirmar_contrasena:
        return {"success": False, "message": "Todos los campos son obligatorios."}

    # Verificar que las contraseñas nuevas coincidan
    if nueva_contrasena != confirmar_contrasena:
        return {"success": False, "message": "Las contraseñas no coinciden."}

    # Verificar que la nueva contraseña tenga al menos 6 caracteres
    if len(nueva_contrasena) < 6:
        return {"success": False, "message": "La contraseña debe tener al menos 6 caracteres."}

    # Obtener token de la sesión y verificar
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get('usuario_id')

    # Obtener el usuario de la base de datos
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}

    # Verificar la contraseña actual
    if not check_password_hash(usuario.contrasena, actual_contrasena):
        return {"success": False, "message": "La contraseña actual es incorrecta."}

    # Si todo es correcto, actualizamos la contraseña
    usuario.contrasena = generate_password_hash(nueva_contrasena)
    db.session.commit()

    return {"success": True, "message": "Contraseña actualizada correctamente."}

from datetime import datetime

# Servicio para obtener el nombre, rol y fecha de registro del usuario autenticado
def obtener_datos_usuario_service():
    token = session.get('jwt')
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
        "tipo_aptitud": aptitudes.tipo_aptitud,
        "institucion": estudios.institucion,
        "titulo_obtenido": estudios.titulo_obtenido,
        "fecha_inicio": estudios.fecha_inicio,
        "fecha_fin": estudios.fecha_fin,
        "nombre": experiencias.nombre,
        "descripcion": experiencias.descripcion,
        "fecha_inicio_experiencia": experiencias.fecha_inicio_experiencia,
        "fecha_fin_experiencia": experiencias.fecha_fin_experiencia,
        "foto_perfil": perfil.foto_perfil,

        "fecha_registro": f"Se unió en {fecha_formateada}"  # Formateamos la fecha
    }

# Servicio para deshabilitar la cuenta
def deshabilitar_cuenta_service(data):
    contrasena = data.get("contrasena")

    if not contrasena:
        return {"success": False, "message": "La contraseña es obligatoria."}

    # Obtener token desde la sesión
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get('usuario_id')
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}

    # Verificar la contraseña
    if not check_password_hash(usuario.contrasena, contrasena):
        return {"success": False, "message": "La contraseña es incorrecta."}

    # Cambiar el estado a 'deshabilitado'
    usuario.estado = "deshabilitado"
    db.session.commit()

    # Cerrar la sesión
    session.pop('jwt', None)

    return {"success": True, "message": "Tu cuenta ha sido deshabilitada correctamente."}





from flask import url_for
# Servicio para enviar enlace de recuperación
def enviar_link_recuperacion_service(correo):

   
    
    # Verificar que el correo no esté vacío
    if not correo:
        return {"success": False, "message": "El correo es obligatorio."}

    # Buscar el usuario por correo
    usuario = Usuario.query.filter_by(correo=correo).first()
    if not usuario:
        return {"success": False, "message": "No existe una cuenta con ese correo."}

    # ✅ Generar un token válido solo para restablecer la contraseña (5 minutos)
    token = generar_token_recuperacion(usuario.usuario_id)



    # ✅ Guardar el token en el campo 'token_recuperacion'
    usuario.token_recuperacion = token
    db.session.commit()  # Guardamos los cambios en la base de datos

    # Construir el enlace
    link = url_for('web.restablecer_contraseña', token=token, _external=True)

    
    perfil=usuario.perfiles
    if not perfil:
        return {"success": False, "message": "perfil no encontrado para el usuario."}
    


    # Aquí es donde realmente se llama a la función de enviar correo
    resultado_envio = enviar_link_recuperacion_correo(
        correo_destino=correo,
        nombre_usuario=perfil.primer_nombre,  # o el campo adecuado que uses para el nombre
        link_recuperacion=link
    )

    if resultado_envio['success']:
        return {"success": True, "message": "Se ha enviado un enlace de recuperación a tu correo."}
    else:
        return {"success": False, "message": f"Ocurrió un error al enviar el correo: {resultado_envio['message']}"}


# Servicio para restablecer la contraseña usando un token
def restablecer_contraseña_service(data):
    token = data.get("token")
    nueva_contraseña = data.get("nueva_contraseña")
    confirmar_contraseña = data.get("confirmar_contraseña")

    # Validar que todos los campos estén presentes
    if not token or not nueva_contraseña or not confirmar_contraseña:
        return {"success": False, "message": "Todos los campos son obligatorios."}

    # Validar que las contraseñas coincidan
    if nueva_contraseña != confirmar_contraseña:
        return {"success": False, "message": "Las contraseñas no coinciden."}

    # Validar longitud mínima de la contraseña
    if len(nueva_contraseña) < 6:
        return {"success": False, "message": "La contraseña debe tener al menos 6 caracteres."}

    # Verificar el token (con la nueva función de verificación)
    resultado_token = verificar_token(token)
    if not resultado_token.get('valid'):
        return {"success": False, "message": resultado_token.get('message', 'El enlace no es válido o ha expirado.')}

    payload = resultado_token.get('payload')

    # Verificar que la acción sea la correcta para restablecer la contraseña
    if payload.get('accion') != 'recuperar_contraseña':
        return {"success": False, "message": "El token no es válido para esta acción."}

    # Verificar si el token está expirado
    if resultado_token.get('reason') == 'expired':
        return {"success": False, "message": "El enlace de recuperación ha expirado. Solicita uno nuevo."}

    usuario_id = payload.get('usuario_id')

    # Obtener el usuario
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return {"success": False, "message": "Usuario no encontrado."}

    # Verificar si el token de recuperación aún está en la base de datos
    if not usuario.token_recuperacion or usuario.token_recuperacion != token:
        return {"success": False, "message": "El token no es válido o ya ha sido utilizado."}

    # Actualizar la contraseña
    usuario.contrasena = generate_password_hash(nueva_contraseña)

    # Eliminar el token de recuperación de la base de datos (lo hace solo una vez)
    usuario.token_recuperacion = None

    # Guardar los cambios en la base de datos
    db.session.commit()

    return {"success": True, "message": "Tu contraseña ha sido actualizada correctamente."}
