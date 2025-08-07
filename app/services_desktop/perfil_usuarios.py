from app.models.usuario import Usuario
from flask import request, session
from app.services.jwt_service import generar_token, verificar_token
from app.models.perfiles import perfiles

# Servicio para ver los perfiles de los usuarios 
def perfil_usuarios_admin_service():
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
    

    # Hacemos un filtro para que nos traiga los perfiles, pero de los usuarios que tengan rol de cliente y experto.
    perfiless = perfiles.query.join(Usuario).filter(Usuario.id_rol.in_([1,2])).all()

    # Guardamos los perfiles en el array lista_perfiles
    lista_perfiles= []

    for  perfil in perfiless:
        lista_perfiles.append({
            "id_perfil": perfil.id_perfil,
            "id_usuario": perfil.id_usuario,
            "primer_nombre": perfil.primer_nombre,
            "segundo_nombre": perfil.segundo_nombre,
            "primer_apellido": perfil.primer_apellido,
            "segundo_apellido": perfil.segundo_apellido,
            "especialidad": perfil.especialidad,
            "direccion": perfil.direccion,
            "foto_perfil": perfil.foto_perfil, 
            "descripcion_perfil": perfil.descripcion_perfil
        })
    
    return {"success": True, "lista_perfiles": lista_perfiles}
