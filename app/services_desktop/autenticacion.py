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

def gestionar_usuarios_admin_service():
    token = session.get('jwt')

      # Si no hay token en sesión, intenta obtenerlo del header Authorization
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    
    if not token:
        return {"success": False, "message": "Token  no enviado."}
    
    
    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario_admin = Usuario.query.filter_by(usuario_id=usuario_id).first()

    if not usuario_admin:
        return{"success": False, "message": "Usuario no encontrado"}
    
    if usuario_admin.id_rol != 3:
        return{"success": False, "message": "No tienes permisos de administrador"}
    
    usuarios = Usuario.query.all()

    lista_usuarios = []

    for usuario in usuarios:
        lista_usuarios.append({
            "usuario_id": usuario.usuario_id,
            "fecha_registro": usuario.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")  if usuario.fecha_registro else None,
            "correo": usuario.correo,
            "estado": usuario.estado,
            "token_recuperacion": usuario.token_recuperacion,
            "intentos_fallidos": usuario.intentos_fallidos,
            "bloqueado_hasta": usuario.bloqueado_hasta.strftime("%Y-%m-%d %H:%M:%S") if usuario.bloqueado_hasta else None,
            "id_rol": usuario.id_rol
        })

    return {"success": True, "usuarios": lista_usuarios}


def deshabilitar_cuentas_admin_service(data):
    token = session.get('jwt')

      # Si no hay token en sesión, intenta obtenerlo del header Authorization
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        return {"success": True, "message": "Token no enviado"}
    
    resultado= verificar_token(token)
    if not resultado["valid"]:
        return {"success": False, "message": "No estas autenticado "}
    
    usuario_id = resultado["payload"].get("usuario_id")
    
    usuario_admin = Usuario.query.filter_by(usuario_id=usuario_id).first()
    
    if not usuario_admin:
        return{"success": False, "message": "Usuario no encontrado"}
    
    if usuario_admin.id_rol != 3:
        return{"success": False, "message": "No tienes permisos de administrador"}

    
    usuario_id = data.get("usuario_id")

    usuario = Usuario.query.filter_by(usuario_id=usuario_id).first()

    if not usuario:
        return {"success": False, "message": "No hay ningun usuario"}
    
    if usuario.estado == "deshabilitado":
        return{"success": False, "message": "El usuario ya esta deshabilitado"}
    
    if usuario.estado == "activo":
        usuario.estado = "deshabilitado"
        db.session.commit()

        return {"success": True, "message": f"El usuario con ID {usuario_id} ha sido deshabilitado"}
    