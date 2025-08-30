import jwt
from flask import current_app
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
TOKENS_REVOCADOS = set()

# Función para generar token de autenticación (EXISTENTE)
def generar_token(usuario_id):
    payload = {
        'usuario_id': usuario_id,
        'exp': datetime.utcnow() + timedelta(hours=12)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

# ✅ NUEVO: Función para generar token de restablecer contraseña (5 minutos)
def generar_token_recuperacion(usuario_id):
    payload = {
        'usuario_id': usuario_id,
        'accion': 'recuperar_contraseña',
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Verificar y decodificar token (función genérica)
def verificar_token(token):
    if token in TOKENS_REVOCADOS:
        return False

    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return {
            "valid": True,
            "payload": payload
        }
    except ExpiredSignatureError:
        return {
            "valid": False,
            "reason": "expired",
            "message": "El enlace ha expirado. Solicita uno nuevo."
        }
    except InvalidTokenError:
        return {
            "valid": False,
            "reason": "invalid",
            "message": "El enlace no es válido. Solicita uno nuevo."
        }