from flask import Blueprint, render_template, current_app,jsonify, request, redirect, url_for, flash, session
from app.services.autenticacion import registrar_usuario_service, iniciar_sesion_service, cerrar_sesion_service,verificar_autenticacion_service,obtener_usuario_id_autenticado
from app.services.configuracion import cambiar_contrasena_service,obtener_datos_usuario_service,deshabilitar_cuenta_service, enviar_link_recuperacion_service,restablecer_contraseña_service
from app.services.perfil_cliente import actualizar_perfil_cliente_service, subir_foto_perfil_service
from app.services.perfil_experto import actualizar_perfil_experto_service, actualizar_perfil_experto_service2, actualizar_perfil_experto_service3,actualizar_perfil_experto_service4
from app.services.perfil_experto import eliminar_idioma, eliminar_aptitud,eliminar_estudios,editar_estudios,actualizar_experiencia,eliminar_experiencia,editar_experiencia
from app.services.perfil_experto import actualizar_perfil_experto_service5,eliminar_descripcion,editar_descripcion, subir_foto_perfil_service_experto
from app.services.rol_service import verificar_rol, cambiar_rol_a_experto_service, cambiar_rol_a_cliente_service
from app.services.mis_publicaciones import obtener_mis_publicaciones_service, obtener_categorias_service, obtener_subcategorias_service, obtener_publicacion_por_id_service, guardar_mi_publicacion_service, eliminar_publicacion_service
from app.services.perfil_publico import obtener_perfil_publico_service
from app.services.guardados import obtener_guardados_service, guardar_publicacion_service, eliminar_guardado_service
from app.services.jwt_service import verificar_token
from flask import send_from_directory

from app.models import Usuario  # Importa el modelo de Usuario
from werkzeug.utils import secure_filename
import os


#librerias para la mensajeria
from flask_login import login_required, current_user, login_user


# Define el Blueprint para las rutas web
web = Blueprint('web', __name__)

from app.services.publi_recientes import obtener_publicaciones_recientes_service, obtener_publicaciones_aleatorias_service
@web.route('/')
def inicio():
    publicaciones_recientes = obtener_publicaciones_recientes_service()
    publicaciones_aleatorias = obtener_publicaciones_aleatorias_service()

    primer_nombre = ""
    auth_result = verificar_autenticacion_service()

    if auth_result.get("authenticated"):
        datos_usuario = obtener_datos_usuario_service()
        primer_nombre = datos_usuario.get("primer_nombre", "").title()

    return render_template(
        'inicio.html',
        primer_nombre=primer_nombre,
        publicaciones_recientes=publicaciones_recientes,
        publicaciones_aleatorias=publicaciones_aleatorias
    )


# Ruta para registrarse (Formulario web)
@web.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        data = request.form.to_dict()
        resultado = registrar_usuario_service(data)

        # Asegurar que la clave 'success' existe y es booleana
        categoria = 'success' if resultado.get("success") else 'error'
        flash(resultado.get("message", "Error inesperado."), categoria)

        if resultado.get("success"):
            return redirect(url_for('index.inicio'))

    return render_template('registrar_usuario.html')

# Ruta para iniciar sesión (Formulario web)
@web.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        data = request.form.to_dict()
        resultado = iniciar_sesion_service(data)

        categoria = 'success' if resultado.get("success") else 'error'
        flash(resultado.get("message", "Error inesperado."), categoria)

        if resultado.get("success"):

            #se añade la funcion login user para mantener la sesion activa (mensajeria)
            usuario = Usuario.query.filter_by(correo=data["correo"]).first()  # Obtener usuario
            login_user(usuario)  # Mantener sesión activa
            return redirect(url_for('index.inicio'))

    return render_template('iniciar_sesion.html')

# Ruta para cerrar sesión
@web.route('/cerrar_sesion', methods=['POST', 'GET'])
def cerrar_sesion():
    cerrar_sesion_service()
    return redirect(url_for('index.inicio'))

# Ruta para la configuración del usuario
@web.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    # Verificar autenticación
    auth_result = verificar_autenticacion_service()
    if not auth_result.get("authenticated"):
        flash(auth_result.get("message"), "error")
        return redirect(url_for('web.iniciar_sesion'))  # o la ruta que quieras para login

    if request.method == 'POST':
        # Aquí solo lanzamos un mensaje o puedes implementar algo después
        flash("Formulario enviado correctamente.", "success")
        return redirect(url_for('web.configuracion'))

    # Obtener los datos del usuario (nombre, rol y fecha de registro)
    resultado = obtener_datos_usuario_service()
    primer_nombre = resultado.get("primer_nombre", "").title()
    primer_apellido = resultado.get("primer_apellido", "").title()
    rol = resultado.get("rol", "").title()
    fecha_registro = resultado.get("fecha_registro", "")

    # Pasamos todos los datos a la plantilla
    return render_template('configuracion.html', primer_nombre=primer_nombre, primer_apellido=primer_apellido, rol=rol, fecha_registro=fecha_registro)


# Ruta para cambiar la contraseña
@web.route('/configuracion/cambiar_contraseña', methods=['POST'])
def cambiar_contraseña():
    # Verificar si el usuario ha iniciado sesión
    auth_result = verificar_autenticacion_service()
    if not auth_result["authenticated"]:
        flash(auth_result["message"], "error")
        return redirect(url_for('index.inicio'))  # O 'web.index'

    data = request.form.to_dict()
    resultado = cambiar_contrasena_service(data)

    categoria = 'success' if resultado.get("success") else 'error'
    flash(resultado.get("message", "Error inesperado."), categoria)

    return redirect(url_for('web.configuracion'))


# Ruta para deshabilitar la cuenta
@web.route('/configuracion/deshabilitar_cuenta', methods=['POST'])
def deshabilitar_cuenta():
    # Verificar si el usuario está autenticado
    auth_result = verificar_autenticacion_service()
    if not auth_result["authenticated"]:
        flash(auth_result["message"], "error")
        return redirect(url_for('index.inicio'))

    data = request.form.to_dict()
    resultado = deshabilitar_cuenta_service(data)

    categoria = 'success' if resultado.get("success") else 'error'
    flash(resultado.get("message", "Error inesperado."), categoria)

    if resultado.get("success"):
        return redirect(url_for('index.inicio'))  # Redirige a la página principal o donde prefieras

    return redirect(url_for('web.configuracion'))


# Ruta para enviar el enlace de recuperación de contraseña
# Esta ruta se activa al enviar el formulario de recuperación
@web.route('/recuperar_contraseña', methods=['GET', 'POST'])
def recuperar_contraseña():
    if request.method == 'POST':
        correo = request.form.get('correo')
        
        resultado = enviar_link_recuperacion_service(correo)

        categoria = 'success' if resultado.get("success") else 'error'
        flash(resultado.get("message", "Error inesperado."), categoria)

        # Después de procesar, volvemos a mostrar el formulario
        return redirect(url_for('web.recuperar_contraseña'))

    # Si es GET, simplemente mostramos el formulario vacío
    return render_template('recuperar_contraseña.html')


# Ruta para restablecer la contraseña
# Esta ruta se activa al hacer clic en el enlace enviado al correo
@web.route('/restablecer_contraseña/<token>', methods=['GET', 'POST'])
def restablecer_contraseña(token):
    if request.method == 'POST':
        nueva_contraseña = request.form.get('contraseña')
        confirmar_contraseña = request.form.get('contraseña2')

        # Preparamos el diccionario que espera la función service
        data = {
            "token": token,
            "nueva_contraseña": nueva_contraseña,
            "confirmar_contraseña": confirmar_contraseña
        }

        resultado = restablecer_contraseña_service(data)

        if resultado['success']:
            flash(resultado['message'], 'success')
            return redirect(url_for('web.iniciar_sesion'))  # O redirige donde prefieras
        else:
            flash(resultado['message'], 'error')

    return render_template('cambiar_contraseña.html')


# Ruta para categorias
@web.route('/categorias')
def categorias():
    return render_template('categorias.html')


# Ruta para perfil cliente
@web.route('/perfil_cliente', methods=['GET', 'POST'])
def perfil_cliente():
    auth_result = verificar_autenticacion_service()
    if not auth_result.get("authenticated"):
        flash(auth_result.get("message"), "error")
        return redirect(url_for('web.iniciar_sesion'))

    if request.method == 'POST':
        form_tipo = request.form.get('form_tipo')
        data = request.form.to_dict()

        if form_tipo == 'foto_perfil':
            file = request.files.get('foto')
            resultado = subir_foto_perfil_service(file)
        else:
            campos_map = {
                'perfil_principal': ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'correo'],
                'direccion': ['direccion'],
            }
            campos = campos_map.get(form_tipo)
            if campos:
                resultado = actualizar_perfil_cliente_service(data, campos=campos)
            else:
                resultado = {"success": False, "message": "Formulario desconocido."}

        flash(resultado.get("message"), "success" if resultado.get("success") else "error")
        return redirect(url_for('web.perfil_cliente'))

    # GET
    datos = obtener_datos_usuario_service()
    return render_template(
        'perfil_cliente.html',
        primer_nombre=datos.get("primer_nombre", "").title(),
        segundo_nombre=(datos.get("segundo_nombre") or "").title(),
        primer_apellido=datos.get("primer_apellido", "").title(),
        segundo_apellido=(datos.get("segundo_apellido") or "").title(),
        direccion=(datos.get("direccion") or "").title(),
        foto_perfil=datos.get("foto_perfil", "")
    )
from werkzeug.utils import secure_filename

@web.route('/uploads/perfiles/<filename>')
def perfil_foto(filename):
    carpeta = os.path.join(current_app.root_path, 'uploads', 'perfiles')
    safe_filename = secure_filename(filename)
    return send_from_directory(carpeta, safe_filename)


# Ruta para visualizar el perfil del experto
@web.route('/perfil_experto', methods=['GET', 'POST'])
def perfil_experto():
    # Verificamos si el usuario está autenticado
    auth_result = verificar_autenticacion_service()
    if not auth_result.get("authenticated"):
        flash(auth_result.get("message"), "error")
        return redirect(url_for('web.iniciar_sesion'))

    if request.method == 'POST':
        form_tipo =   request.form.get('form_tipo1') or  request.form.get('form_tipo2') or request.form.get('form_tipo3') or request.form.get('form_tipo4') or request.form.get('form_tipo5') or request.form.get('form_tipo6')   # Obtiene el tipo de formulario enviado
        data = request.form.to_dict()

        if form_tipo == 'perfil_principal2':
            # Actualizar solo campos principales
            campos = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']
            resultado = actualizar_perfil_experto_service(data, campos=campos)
        
        elif form_tipo == 'idioma':
             campos=['nombre_idioma']
             resultado =  actualizar_perfil_experto_service2(data, campos=campos)
        
        elif form_tipo == 'aptitud':
            campos = ['tipo_aptitud']
            resultado = actualizar_perfil_experto_service3(data, campos=campos)
        
        elif form_tipo == 'estudios':
             campos= ['institucion', 'titulo_obtenido', 'fecha_inicio', 'fecha_fin']
             resultado = actualizar_perfil_experto_service4(data, campos=campos)

        elif form_tipo == 'eliminar_idioma':
            resultado = eliminar_idioma(data)

        elif form_tipo == 'eliminar_aptitud':
            resultado = eliminar_aptitud(data)
        
        elif form_tipo == 'eliminar_estudios':
            resultado = eliminar_estudios(data)

        elif form_tipo == 'editar_estudios':
            resultado = editar_estudios(data)

        elif form_tipo == 'experiencia':
            resultado = actualizar_experiencia(data)

        elif form_tipo == 'eliminar_experiencia':
            resultado = eliminar_experiencia(data)
        
        elif form_tipo == 'editar_experiencia':
            resultado = editar_experiencia(data)

        elif form_tipo == 'perfil_principal3':
            resultado = actualizar_perfil_experto_service5(data)

        elif form_tipo == 'eliminar_descripcion':
            resultado = eliminar_descripcion(data)
        
        elif form_tipo == 'editar_descripcion':
            resultado = editar_descripcion(data)
        
        elif form_tipo == 'foto_perfil':
             file = request.files.get('foto')
             resultado = subir_foto_perfil_service_experto(file)

        else:
            resultado = {"success": False, "message": "Formulario desconocido."}
        
        categoria = 'success' if resultado.get("success") else 'error'
        flash(resultado.get("message", "Error al actualizar perfil."), categoria)
        return redirect(url_for('web.perfil_experto'))

    resultado = obtener_datos_usuario_service()
    
    return render_template(
        'perfil_experto.html', 
        id_perfil=resultado.get("id_perfil", ""),
        primer_nombre= resultado.get("primer_nombre", "").title(),
        segundo_nombre = (resultado.get("segundo_nombre") or "").title(), 
        primer_apellido = resultado.get("primer_apellido", "").title(),
        segundo_apellido = (resultado.get("segundo_apellido") or "").title(),
        descripcion_perfil = (resultado.get("descripcion_perfil") or "").title(),
        nombre_idioma = (resultado.get("nombre_idioma") or "").title(),
        tipo_aptitud = (resultado.get("tipo_aptitud") or "").title(),
        institucion = (resultado.get("institucion") or "").title(),
        titulo_obtenido = (resultado.get("titulo_obtenido") or "").title(), 
        fecha_inicio = resultado.get("fecha_inicio", ""),
        fecha_fin = resultado.get("fecha_fin", ""),
        nombre_experiencia = (resultado.get("nombre") or "").title(),
        descripcion_experiencia = (resultado.get("descripcion") or "").title(),
        fecha_inicio_experiencia = resultado.get("fecha_inicio_experiencia", ""),
        fecha_fin_experiencia = resultado.get("fecha_fin_experiencia", ""),
        foto_perfil=resultado.get("foto_perfil", "")

        )
        
    

# Ruta para visualizar el chat
@web.route('/mensajeria.html')
def mensajeria():
    return render_template('mensajeria.html')

# Ruta para la sección de guardados (requiere sesión)
@web.route('/guardar-publicacion/<int:publicacion_id>', methods=['POST'])
def guardar_publicacion(publicacion_id):
    try:
        resultado = guardar_publicacion_service(publicacion_id)
        return jsonify(resultado), (200 if resultado["success"] else 400)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(success=False, message=f"Error interno: {str(e)}"), 500


@web.route('/mis_guardados')
def guardados():
    
    publicaciones = obtener_guardados_service()
    return render_template('guardados.html', publicaciones=publicaciones)

# Ruta para eliminar un guardado@web.route('/mis-guardados/eliminar/<int:publicacion_id>')
@web.route('/mis-guardados/eliminar/<int:publicacion_id>', methods=['POST'])
def eliminar_guardado(publicacion_id):
    usuario_id = obtener_usuario_id_autenticado()
    if not usuario_id:
        return jsonify(success=False, message="Debes iniciar sesión para eliminar guardados"), 401

    resultado = eliminar_guardado_service(publicacion_id)
    return jsonify(success=resultado['success'], message=resultado['message'])

# Ruta para publicaciones del experto

@web.route('/convertirse_en_experto')
def convertir_a_experto():
    resultado = cambiar_rol_a_experto_service()
    flash(resultado.get("message"), "success" if resultado.get("success") else "error")
    return redirect(url_for('web.perfil_experto'))



@web.route('/convertirse_en_cliente')
def convertir_a_cliente():
    resultado = cambiar_rol_a_cliente_service()
    flash(resultado.get("message"), "success" if resultado.get("success") else "error")
    return redirect(url_for('web.perfil_cliente'))


@web.route('/perfil')
def perfil_general():
    auth_result = verificar_autenticacion_service()
    if not auth_result.get("authenticated"):
        flash(auth_result.get("message"), "error")
        return redirect(url_for('web.iniciar_sesion'))

    usuario_id = obtener_usuario_id_autenticado()
    if not usuario_id:
        flash("No se pudo identificar al usuario.", "error")
        return redirect(url_for('web.inicio'))

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for('web.inicio'))

    if usuario.id_rol == 2:
        return redirect(url_for('web.perfil_cliente'))
    elif usuario.id_rol == 1:
        return redirect(url_for('web.perfil_experto'))
    else:
        flash("Rol no reconocido.", "error")
        return redirect(url_for('web.inicio'))


#perfil general
@web.route('/perfil-experto/<int:usuario_id>')
def perfil_experto_publico(usuario_id):
    experto = Usuario.query.get(usuario_id)
    if not experto:
        flash("No se encontró el usuario.", "error")
        return redirect(url_for('web.inicio'))

    perfil = obtener_perfil_publico_service(usuario_id)

    # Si tu modelo Usuario no tiene las relaciones directas y las maneja el modelo 'perfiles', puedes acceder desde perfil
    experiencias = perfil.experiencias if perfil else []
    idiomas = perfil.idioma if perfil else []
    aptitudes = perfil.aptitudes if perfil else []
    descripcion_perfil = perfil.descripcion_perfil if perfil else []
    estudios = perfil.estudios if perfil else []

    return render_template(
        'perfil_experto_publico.html',
        experto=experto,
        perfil=perfil,
        experiencias=experiencias,
        idiomas=idiomas,
        aptitudes=aptitudes,
        descripcion_perfil=descripcion_perfil,
        estudios=estudios,
    )








from app.models import Categorias  # Adjust path if needed
from app.models import Subcategorias, Publicaciones, perfiles  # Adjust path if needed
  



@web.route('/mis-publicaciones')
def mis_publicaciones():
    usuario_id = obtener_usuario_id_autenticado()

    if not usuario_id:
        flash("Debes iniciar sesión para ver tus publicaciones", "warning")
        return redirect(url_for('web.login'))

    publicaciones = obtener_mis_publicaciones_service(usuario_id)
    categorias = obtener_categorias_service()
    subcategorias = obtener_subcategorias_service()

     # Calcula si hay publicaciones válidas
    tiene_publicaciones = any(
    pub.titulo and pub.descripcion_publicacion
    for pub in publicaciones
    )

    return render_template(
        'mis_publicaciones.html',
        publicaciones=publicaciones,
        categorias=categorias,
        subcategorias=subcategorias,
        publicacion=None,
        tiene_publicaciones=tiene_publicaciones,
    )

@web.route('/mis-publicaciones/guardar', methods=['POST'])
def guardar_mi_publicacion():
    usuario_id = obtener_usuario_id_autenticado()
    if not usuario_id:
        flash("Debes iniciar sesión para realizar esta acción", "warning")
        return redirect(url_for('web.login'))  # Ajusta tu ruta

    data = dict(request.form)
    data['usuario_id'] = usuario_id

    resultado = guardar_mi_publicacion_service(data)
    flash(resultado['message'], 'success' if resultado['success'] else 'danger')
    return redirect(url_for('web.mis_publicaciones'))



@web.route('/mis-publicaciones/editar/<int:publicacion_id>')
def editar_mi_publicacion(publicacion_id):
    usuario_id = obtener_usuario_id_autenticado()
    if not usuario_id:
        flash("Debes iniciar sesión para editar tus publicaciones", "warning")
        return redirect(url_for('web.login'))

    publicaciones = obtener_mis_publicaciones_service(usuario_id)
    categorias = obtener_categorias_service()
    subcategorias = obtener_subcategorias_service()
    publicacion = obtener_publicacion_por_id_service(publicacion_id)

    # Valida que la publicación sea del usuario autenticado
    if not publicacion or publicacion.usuario_id != usuario_id:
        flash("No tienes permiso para editar esta publicación", "danger")
        return redirect(url_for('web.mis_publicaciones'))

    # Calcula si hay publicaciones válidas
    tiene_publicaciones = any(
        pub.titulo and pub.descripcion_publicacion
        for pub in publicaciones
    )

    return render_template(
        'mis_publicaciones.html',
        publicaciones=publicaciones,
        categorias=categorias,
        subcategorias=subcategorias,
        publicacion=publicacion,
        tiene_publicaciones=tiene_publicaciones
    )




@web.route('/mis-publicaciones/eliminar/<int:publicacion_id>')
def eliminar_mi_publicacion(publicacion_id):
    usuario_id = obtener_usuario_id_autenticado()
    if not usuario_id:
        flash("Debes iniciar sesión para eliminar publicaciones", "warning")
        return redirect(url_for('web.login'))

    publicacion = obtener_publicacion_por_id_service(publicacion_id)
    
    if not publicacion:
        flash("La publicación no existe", "danger")
        return redirect(url_for('web.mis_publicaciones'))

    if publicacion.usuario_id != usuario_id:
        flash("No tienes permiso para eliminar esta publicación", "danger")
        return redirect(url_for('web.mis_publicaciones'))

    resultado = eliminar_publicacion_service(publicacion_id)
    flash(resultado['message'], 'success' if resultado['success'] else 'danger')

    return redirect(url_for('web.mis_publicaciones'))
