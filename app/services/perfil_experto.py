from flask import session,  current_app
from app.services.jwt_service import verificar_token
from app.models.usuario import Usuario
from app.models.perfiles import perfiles
from app.models.idiomas import Idiomas
from app.models.aptitudes import Aptitudes
from app.extensions import db
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os


def obtener_usuario_id():
    token = session.get('jwt')
    if not token:
        return None, "No estás autenticado."

    resultado = verificar_token(token)
    if not resultado["valid"]:
        return None, resultado["message"]

    return resultado["payload"].get("usuario_id"), None

def actualizar_perfil_experto_service(data, campos=None):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    # Si no se indican campos, actualiza todo
    if campos is None:
        campos = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']

    for campo in campos:
        if campo in data:
            setattr(perfil, campo, data[campo])

    try:
        db.session.commit()
        return {"success": True, "message": "perfil actualizado correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al actualizar perfil: {str(e)}"}

def actualizar_perfil_experto_service2(data, campos=None):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil = perfiles.query.filter_by(id_usuario=usuario_id).first()
    
    if not perfil:
        return {"success": False, "message": "Perfil no encontrado."}

    nombre_idioma = data.get('nombre_idioma')
    print(f"Nombre del idioma recibido: {nombre_idioma}")

    idioma = Idiomas.query.filter_by(nombre_idioma=nombre_idioma).first()
    if not idioma:
        return {"success": False, "message": "Idioma no encontrado."}

    #  Verificar si ya hay 3 idiomas asociados al perfil
    cantidad_idiomas = db.session.execute(
        text("SELECT COUNT(*) FROM perfil_idioma WHERE id_perfil = :perfil_id"),
        {"perfil_id": perfil.id_perfil}
    ).scalar()

    if cantidad_idiomas >= 3:
        return {"success": False, "message": "Solo puedes añadir hasta 3 idiomas."}

    #  Verificar si ya existe esa relación
    relacion_existente = db.session.execute(
        text("SELECT * FROM perfil_idioma WHERE id_perfil = :perfiles AND idioma_id = :idiomas"),
        {"perfiles": perfil.id_perfil, "idiomas": idioma.idioma_id}
    ).fetchone()
    
    if relacion_existente:
        return {"success": False, "message": "El idioma ya está asociado a este perfil."}

    try:
        db.session.execute(
            text("INSERT INTO perfil_idioma (id_perfil, idioma_id) VALUES (:perfil, :idioma)"),
            {"perfil": perfil.id_perfil, "idioma": idioma.idioma_id}
        )
        db.session.commit()
        return {"success": True, "message": "Idioma añadido correctamente al perfil."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al añadir idioma: {str(e)}"}
 
def actualizar_perfil_experto_service3(data, campos=None):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")
    perfil = perfiles.query.filter_by(id_usuario=usuario_id).first()

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    tipo_aptitud = data.get('tipo_aptitud')
    if not tipo_aptitud:
        return {"success": False, "message": "Tipo de aptitud no proporcionado."}

    #  Verificar si ya hay 3 aptitudes registradas
    cantidad = db.session.execute(
        text("SELECT COUNT(*) FROM aptitudes WHERE id_perfil = :perfil AND tipo_aptitud IS NOT NULL"),
        {"perfil": perfil.id_perfil}
    ).scalar()

    if cantidad >= 3:
        return {"success": False, "message": "Solo puedes registrar hasta 3 aptitudes."}

    try:
        #  Inserta una nueva aptitud
        db.session.execute(
            text("INSERT INTO aptitudes (id_perfil, tipo_aptitud) VALUES (:perfil, :tipo_aptitud)"),
            {"perfil": perfil.id_perfil, "tipo_aptitud": tipo_aptitud}
        )
        db.session.commit()
        return {"success": True, "message": "Aptitud agregada correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al agregar aptitud: {str(e)}"}



def actualizar_perfil_experto_service4(data, campos= None ):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    institucion = data.get('institucion')
    titulo_obtenido = data.get('titulo_obtenido')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')

    
    
    datos = {
        "institucion": institucion,
        "titulo_obtenido": titulo_obtenido,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }
    
    if not datos:
        return {"success": False, "message": "Datos no proporcionado."}

    print(f"Datos de educación recibidos: {datos}") 
   
    try:
        db.session.execute(
            text("UPDATE estudios SET institucion  =:institucion,  titulo_obtenido =:titulo_obtenido,  fecha_inicio =:fecha_inicio,  fecha_fin =:fecha_fin  WHERE id_perfil = :perfil"),
            {"institucion": institucion, "titulo_obtenido": titulo_obtenido , "fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "perfil": perfil.id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Estudios  agregados correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al agregar estudios: {str(e)}"}
    
   
def obtener_idiomas_perfil():
    token = session.get('jwt')
    if not token:
        return []

    resultado = verificar_token(token)
    if not resultado["valid"]:
        return []

    usuario_id = resultado["payload"].get("usuario_id")
    perfil = perfiles.query.filter_by(id_usuario=usuario_id).first()

    if not perfil:
        return []

    resultados = db.session.execute(
        text("""
            SELECT i.idioma_id, i.nombre_idioma 
            FROM perfil_idioma pi
            JOIN idiomas i ON i.idioma_id = pi.idioma_id
            WHERE pi.id_perfil = :perfil_id
        """),
        {"perfil_id": perfil.id_perfil}
    ).fetchall()

    # Agregamos también el ID del idioma 
    return [{"id": fila[0], "nombre": fila[1]} for fila in resultados]


def eliminar_idioma(data):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")
    perfil = perfiles.query.filter_by(id_usuario=usuario_id).first()

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    id_perfil = data.get('id_perfil')
    idioma_id = data.get('idioma_id')  #  Aquí el nombre correcto

    if not id_perfil or not idioma_id:
        return {"success": False, "message": "Faltan datos para eliminar el idioma."}

    try:
        db.session.execute(
            text("DELETE FROM perfil_idioma WHERE id_perfil = :perfil AND idioma_id = :idioma"),
            {"perfil": id_perfil, "idioma": idioma_id}
        )
        db.session.commit()
        return {"success": True, "message": "Idioma eliminado correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al eliminar idioma: {str(e)}"}

def obtener_aptitudes_perfil(id_perfil):
    resultados = db.session.execute(
        text("SELECT tipo_aptitud FROM aptitudes WHERE id_perfil = :perfil AND tipo_aptitud IS NOT NULL"),
        {"perfil": id_perfil}
    ).fetchall()

    return [{"tipo_aptitud": fila[0]} for fila in resultados]

def eliminar_aptitud(data):
    id_perfil = data.get("id_perfil")
    tipo_aptitud = data.get("tipo_aptitud")

    try:
        db.session.execute(
            text("DELETE FROM aptitudes WHERE id_perfil = :id_perfil AND tipo_aptitud = :tipo_aptitud"),
            {"id_perfil": id_perfil, "tipo_aptitud": tipo_aptitud}
        )
        db.session.commit()
        return {"success": True, "message": "Aptitud eliminada correctamente"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al eliminar aptitud: {str(e)}"}

def eliminar_estudios(data):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    id_perfil = data.get('id_perfil')
    
    
    if not id_perfil:
        return {"success": False, "message": "ID  no proporcionado."}

   
    try:
        db.session.execute(
            text("UPDATE estudios SET institucion =:institucion, titulo_obtenido =:titulo, fecha_inicio =:fecha_inicio,  fecha_fin =:fecha_fin  WHERE id_perfil = :perfil"),
            { "institucion": None, "titulo": None, "fecha_inicio": None, "fecha_fin":None ,"perfil": id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Estudios borrados correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al eliminar los estudios: {str(e)}"}
    

def editar_estudios(data):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    institucion = data.get('institucion')
    titulo_obtenido = data.get('titulo_obtenido')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')

    
    
    datos = {
        "institucion": institucion,
        "titulo_obtenido": titulo_obtenido,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }
    
    if not datos:
        return {"success": False, "message": "Datos no proporcionado."}

    print(f"Datos de educación recibidos: {datos}") 
   
    try:
        db.session.execute(
            text("UPDATE estudios SET institucion  =:institucion,  titulo_obtenido =:titulo_obtenido,  fecha_inicio =:fecha_inicio,  fecha_fin =:fecha_fin  WHERE id_perfil = :perfil"),
            {"institucion": institucion, "titulo_obtenido": titulo_obtenido , "fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "perfil": perfil.id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Estudios  editados correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al editar estudios: {str(e)}"}
    

def actualizar_experiencia(data):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    nombre= data.get('nombre')
    descripcion = data.get('descripcion')
    fecha_inicio_experiencia = data.get('fecha_inicio_experiencia')
    fecha_fin_experiencia = data.get('fecha_fin_experiencia')
    
   

    if not nombre or not descripcion or not fecha_inicio_experiencia or not fecha_fin_experiencia:
        return {"success": False, "message": "Datos de experiencias faltan."}

   
    try:
        db.session.execute(
            text("UPDATE experiencias SET nombre  =:nombre, descripcion =:descripcion, fecha_inicio_experiencia =:fecha_inicio_experiencia, fecha_fin_experiencia =:fecha_fin_experiencia  WHERE id_perfil = :perfil"),
            {"nombre": nombre, "descripcion":descripcion, "fecha_inicio_experiencia":fecha_inicio_experiencia, "fecha_fin_experiencia":fecha_fin_experiencia ,"perfil": perfil.id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Experiencia  agregada correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al actualizar la experiencia: {str(e)}"}


def eliminar_experiencia(data):

    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    id_perfil = data.get('id_perfil')
    
    
    if not id_perfil:
        return {"success": False, "message": "ID  no proporcionado."}

   
    try:
        db.session.execute(
            text("UPDATE experiencias SET nombre =:nombre, descripcion =:descripcion, fecha_inicio_experiencia =:fecha_inicio_experiencia,  fecha_fin_experiencia =:fecha_fin_experiencia  WHERE id_perfil = :perfil"),
            { "nombre": None, "descripcion": None, "fecha_inicio_experiencia": None, "fecha_fin_experiencia":None ,"perfil": id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Experiencia borrada correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al eliminar la experiencia: {str(e)}"}
    

def editar_experiencia(data):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}
    
    id_perfil = data.get('id_perfil')
    nombre = data.get('nombre')
    descripcion= data.get('descripcion')
    fecha_inicio_experiencia = data.get('fecha_inicio_experiencia')
    fecha_fin_experiencia = data.get('fecha_fin_experiencia')

    
    if not nombre or not id_perfil or not descripcion or not fecha_inicio_experiencia or not fecha_fin_experiencia:
        return {"success": False, "message": "Datos de experiencias faltan."}
    
    
   
    try:
        db.session.execute(
            text("UPDATE experiencias SET nombre  =:nombre,  descripcion =:descripcion,  fecha_inicio_experiencia =:fecha_inicio_experiencia,  fecha_fin_experiencia =:fecha_fin_experiencia  WHERE id_perfil = :perfil"),
            {"nombre": nombre, "descripcion":  descripcion, "fecha_inicio_experiencia": fecha_inicio_experiencia, "fecha_fin_experiencia": fecha_fin_experiencia, "perfil": id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Experiencia  editada correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al editar experiencia: {str(e)}"}
    
def actualizar_perfil_experto_service5(data):
    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    
    descripcion_perfil = data.get('descripcion_perfil')
    id_perfil = data.get('id_perfil')
    
   

    if not descripcion_perfil:
        return {"success": False, "message": "No hay datos de descripcion proporcionados."}

   
    try:
        db.session.execute(
            text("UPDATE perfiles SET descripcion_perfil  =:descripcion_perfil  WHERE id_perfil = :perfil"),
            {"descripcion_perfil":descripcion_perfil ,"perfil": id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Descripcion  agregada correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al agregar la descripcion: {str(e)}"}
    

def eliminar_descripcion(data):

    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}

    id_perfil = data.get('id_perfil')
    
    
    if not id_perfil:
        return {"success": False, "message": "ID  no proporcionado."}

   
    try:
        db.session.execute(
            text("UPDATE perfiles SET descripcion_perfil =:descripcion_perfil   WHERE id_perfil = :perfil"),
            { "descripcion_perfil": None ,"perfil": id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Descripcion borrada correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al eliminar la descripcion: {str(e)}"}
    

def editar_descripcion(data):

    token = session.get('jwt')
    if not token:
        return {"success": False, "message": "No estás autenticado."}

    resultado_token = verificar_token(token)
    if not resultado_token["valid"]:
        return {"success": False, "message": resultado_token["message"]}

    usuario_id = resultado_token["payload"].get("usuario_id")

    perfil=perfiles.query.filter_by(id_usuario=usuario_id).first()

    

    if not perfil:
        return {"success": False, "message": "Usuario no encontrado."}
    
    id_perfil = data.get('id_perfil')
    descripcion_perfil = data.get('descripcion_perfil')

    
    if not descripcion_perfil:
        return {"success": False, "message": "Datos de descripcion faltan."}
    
    
   
    try:
        db.session.execute(
            text("UPDATE perfiles SET descripcion_perfil  =:descripcion_perfil    WHERE id_perfil = :perfil"),
            {"descripcion_perfil": descripcion_perfil,  "perfil": id_perfil} 
        )
        db.session.commit()
        return {"success": True, "message": "Descripcion  editada correctamente."}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error al editar descripcion: {str(e)}"}
    

def subir_foto_perfil_service_experto(file):
    if not file or file.filename == '':
        return {"success": False, "message": "No se seleccionó ninguna imagen."}

    usuario_id, error = obtener_usuario_id()
    if error:
        return {"success": False, "message": error}

    perfil = perfiles.query.filter_by(id_usuario=usuario_id).first()
    if not perfil:
        return {"success": False, "message": "Perfil no encontrado."}

    filename = secure_filename(file.filename)
    carpeta = os.path.join(current_app.root_path, 'static', 'uploads', 'perfiles')
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

def insertar_perfil_id(id_perfil_generado):
   
    print(f"ID del perfil recibido: {id_perfil_generado}")

    
    if not id_perfil_generado:
        return {"success": False, "message": "ID del perfil no encontrado."}  
    
    
    
    tablas=["aptitudes", "estudios", "experiencias"]
    
    try:
        for tabla in tablas:
            db.session.execute(text(f"INSERT INTO {tabla} (id_perfil) VALUES (:perfil)"),{"perfil": id_perfil_generado},)
       
            db.session.commit()
           
    except Exception as e:
        db.session.rollback()
        