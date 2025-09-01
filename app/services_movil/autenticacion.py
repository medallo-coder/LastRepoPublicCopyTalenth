from app.services.jwt_service import generar_token, verificar_token
from app.services.notificaciones import enviar_notificacion_registro
from app.services.perfil_experto import insertar_perfil_id
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.usuario import Usuario
from app.models.perfiles import perfiles
from app.models.aptitudes import Aptitudes
from app.models.estudios import Estudios
from app.models.experiencias import Experiencias
from app.models.publicaciones import Publicaciones
from app.models.reseñas import Reseñas
from app.extensions import db
from flask import request, session
from datetime import datetime, timedelta
import re



# Servicio para registrar usuario
def registrar_usuario_service(data):
    primer_nombre = data.get('primer_nombre')
    primer_apellido = data.get('primer_apellido')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    confirmar_contrasena = data.get('confirmar_contrasena')

    if not primer_nombre or not primer_apellido  or not correo or not contrasena or not confirmar_contrasena:
        return {"success": False, "message": "Todos los campos son obligatorios. Por favor, completa cada uno."}

    if len(contrasena) < 6:
        return {"success": False, "message": "La contraseña debe tener al menos 6 caracteres. Intenta con una más larga."}

    if not re.search(r'[A-Z]', contrasena):
        return {"success": False, "message": "La contraseña debe incluir al menos una letra mayúscula. Ejemplo: 'Contraseña123'."}

    if contrasena != confirmar_contrasena:
        return {"success": False, "message": "Las contraseñas no coinciden. Asegúrate de escribirlas igual."}

    if Usuario.query.filter_by(correo=correo).first():
        return {"success": False, "message": "Este correo ya está registrado. Intenta iniciar sesión o usa otro correo."}

    nuevo_usuario = Usuario( 
        correo=correo,
        contrasena=generate_password_hash(contrasena)
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    id_usuario_generado = nuevo_usuario.usuario_id

    nuevo_perfil = perfiles(
        id_usuario=id_usuario_generado,
        primer_nombre=primer_nombre,
        primer_apellido=primer_apellido,
    )
    db.session.add(nuevo_perfil)
    db.session.flush()

    id_perfil_generado = nuevo_perfil.id_perfil


    db.session.commit()

    token = generar_token(nuevo_usuario.usuario_id)

    insertar_perfil_id(id_perfil_generado)

    # Enviar notificación
    enviar_notificacion_registro(correo, primer_nombre)

    if request.is_json:
        return {"success": True, "message": "Registro exitoso", "token": token}

    session['jwt'] = token
    return {"success": True, "message": "Usuario registrado exitosamente."}


# Servicio para iniciar sesion como administrador
def iniciar_sesion_service(data):
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    if not correo or not contrasena:
        return {"success": False, "message": "Debes ingresar tanto el correo como la contrasena."}

    usuario = Usuario.query.filter_by(correo=correo).first()

    if not usuario:
        return {"success": False, "message": "No se encontró una cuenta con ese correo. Verifica que esté bien escrito o regístrate."}

    # Verificar si el usuario está deshabilitado
    if usuario.estado == "deshabilitado":
        return {"success": False, "message": "Usuario deshabilitado. Por favor, regístrate nuevamente con un correo diferente."}
    
    # Solo inician sesion los administradores
    if usuario.id_rol not in(1,2):
        return{"success": False, "message": "Solo se permiten clientes y expertos." }

    # Si ya se acabo el plazo del bloqueo temporal te restablece los intentos  y el estado
    if usuario.estado == "Bloqueado temporalmente" and usuario.bloqueado_hasta and datetime.utcnow() >= usuario.bloqueado_hasta:
        print("⚠️ Periodo de bloqueo ha terminado, restableciendo usuario.")
        usuario.intentos_fallidos = 0
        usuario.estado = "activo"
        usuario.bloqueado_hasta = None
        db.session.commit()
        

    # Verifica cuantos minutos te faltan para desbloquearte
    if usuario.bloqueado_hasta and datetime.utcnow() < usuario.bloqueado_hasta:
        tiempo_restante = usuario.bloqueado_hasta - datetime.utcnow()
        minutos = int(tiempo_restante.total_seconds() // 60)
        return {"success": False, "message": f"Usuario bloqueado temporalmente. Espera {minutos} minutos."}
    
    

    # Verifica si la contraseña es correcta en caso de no ser asi y superes el numero de intentos te bloquea por una hora
    if not check_password_hash(usuario.contrasena, contrasena):
        usuario.intentos_fallidos +=1
        if usuario.intentos_fallidos == 3:
            usuario.estado = "Bloqueado temporalmente"
            usuario.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=5)
        db.session.commit()
        return {"success": False, "message": f"La contrasena es incorrecta. Intento {usuario.intentos_fallidos}."}
    
    

    usuario.intentos_fallidos = 0
    usuario.estado= "activo"
    usuario.bloqueado_hasta = None

    db.session.commit()

    # Genera el token para que el usuario pueda iniciar sesion
    token = generar_token(usuario.usuario_id)

    if request.is_json:
        return {"success": True, "message": "Inicio de sesión exitoso", "token": token}

    session['jwt'] = token
    return {"success": True, "message": "Inicio de sesión exitoso."}

# Lista global o base de datos para tokens revocados
TOKENS_REVOCADOS = set()
# Servicio para cerrar sesion en el apartado administrador
def cerrar_sesion_service(token: str):
    """
    token: el JWT enviado por el header Authorization
    """
    if token:
        TOKENS_REVOCADOS.add(token)  # marca el token como revocado
    return {"success": True, "message": "Sesión cerrada correctamente."}

def verificar_autenticacion_service(token):
    
    if not token:
        return {
            "authenticated": False,
            "message": "No has iniciado sesión. Por favor inicia sesión o regístrate para continuar."
        }

    resultado = verificar_token(token)

    if not resultado.get("valid"):
        session.pop('jwt', None)
        return {
            "authenticated": False,
            "message": "Tu sesión ha expirado. Por favor inicia sesión nuevamente."
        }

    return {
        "authenticated": True,
        "usuario_id": resultado.get("payload", {}).get("usuario_id")
    }

def obtener_usuario_id_autenticado():
    
    token = session.get('jwt')
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        return None

    resultado = verificar_token(token)
    if not resultado.get("valid"):
        return None

    return resultado.get("payload", {}).get("usuario_id")