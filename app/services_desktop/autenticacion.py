from app.models.usuario import Usuario
from werkzeug.security import check_password_hash, generate_password_hash
from app.services.jwt_service import generar_token, verificar_token
from flask import request, session
from app.extensions import db
from datetime import datetime, timedelta

def registrar_admin_service(data):
    correo= data.get('correo')

    if not correo:
        return {"success": False, "message": "Debes ingresar un correo."}
    
    usuario = Usuario.query.filter_by(correo=correo).first()

    if not usuario:
        return {"success": False, "message": "No se encontró una cuenta con ese correo. Verifica que esté bien escrito o regístrate."}
    
    usuario.id_rol = 3

    db.session.commit()
    token = generar_token(usuario.usuario_id)

    if request.is_json:
        return {"success": True, "message": "Registro exitoso", "token": token}

    session['jwt'] = token
    return {"success": True, "message": "Usuario registrado exitosamente."}
    



def iniciar_sesion_admin_service(data):
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

    
    if usuario.bloqueado_hasta and datetime.utcnow() < usuario.bloqueado_hasta:
        tiempo_restante = usuario.bloqueado_hasta - datetime.utcnow()
        minutos = int(tiempo_restante.total_seconds() // 60)
        return {"success": False, "message": f"Usuario bloqueado temporalmente. Espera {minutos} minutos."}
    
    if usuario.estado == "Bloqueado temporalmente" and usuario.bloqueado_hasta and datetime.utcnow() >= usuario.bloqueado_hasta:
        print("⚠️ Periodo de bloqueo ha terminado, restableciendo usuario.")
        usuario.intentos_fallidos = 0
        usuario.estado = "activo"
        usuario.bloqueado_hasta = None
        db.session.commit()

    if not check_password_hash(usuario.contrasena, contrasena):
        usuario.intentos_fallidos +=1
        if usuario.intentos_fallidos == 3:
            usuario.estado = "Bloqueado temporalmente"
            usuario.bloqueado_hasta = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return {"success": False, "message": f"La contrasena es incorrecta. Intento {usuario.intentos_fallidos}."}
    
    if usuario.id_rol != 3:
        return{"success": False, "message": "Solo se permiten usuarios administradores." }

    usuario.intentos_fallidos = 0
    db.session.commit()

    token = generar_token(usuario.usuario_id)

    if request.is_json:
        return {"success": True, "message": "Inicio de sesión exitoso", "token": token}

    session['jwt'] = token
    return {"success": True, "message": "Inicio de sesión exitoso."}

def cerrar_sesion_admin_service():
    session.pop('jwt', None)
    return {"success": True, "message": "Sesión cerrada correctamente."}






