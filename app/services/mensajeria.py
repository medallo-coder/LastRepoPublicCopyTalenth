from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.extensions import db
from app.models.mensajeria import Mensajeria
from app.models.usuario import Usuario
from app.models.perfiles import perfiles  # ✅ Corrección: nombre del archivo y clase
from datetime import datetime

mensajeria_bp = Blueprint('mensajeria', __name__, url_prefix='/mensajeria')

@mensajeria_bp.route('/')
@login_required
def mensajeria():
    return render_template('mensajeria.html', current_user=current_user)

@mensajeria_bp.route('/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    id_emisor = data.get('id_emisor')
    id_receptor = data.get('id_receptor')
    texto = data.get('texto')

    if not id_emisor or not id_receptor or not texto:
        return jsonify({'error': 'Faltan campos requeridos.'}), 400

    mensaje = Mensajeria(
        id_emisor=id_emisor,
        id_receptor=id_receptor,
        texto=texto,
        fecha=datetime.utcnow()
    )
    db.session.add(mensaje)
    db.session.commit()

    return jsonify({'message': 'Mensaje enviado correctamente.'}), 201

@mensajeria_bp.route('/conversaciones/<int:usuario_id>', methods=['GET'])
def obtener_conversaciones(usuario_id):
    mensajes = Mensajeria.query.filter(
        (Mensajeria.id_emisor == usuario_id) | (Mensajeria.id_receptor == usuario_id)
    ).order_by(Mensajeria.fecha.desc()).all()

    if not mensajes:
        return jsonify([]), 200

    contactos = {}
    for m in mensajes:
        otro_id = m.id_receptor if m.id_emisor == usuario_id else m.id_emisor
        if otro_id not in contactos:
            user = Usuario.query.get(otro_id)
            perfil = perfiles.query.filter_by(id_usuario=otro_id).first()

            nombre = (f"{perfil.primer_nombre or ''} {perfil.primer_apellido or ''}".strip()
                      if perfil and perfil.primer_nombre else user.correo.split('@')[0])
            foto = perfil.foto_perfil if perfil and perfil.foto_perfil else 'default.jpg'

            contactos[otro_id] = {
                'usuario_id': user.usuario_id,
                'correo': user.correo,
                'nombre': nombre,
                'foto': foto,
                'ultimo_mensaje': m.texto,
                'fecha': m.fecha.strftime('%Y-%m-%d %H:%M:%S')
            }

    return jsonify(list(contactos.values())), 200

@mensajeria_bp.route('/<int:id_emisor>/<int:id_receptor>', methods=['GET'])
def obtener_mensajes(id_emisor, id_receptor):
    mensajes = Mensajeria.query.filter(
        ((Mensajeria.id_emisor == id_emisor) & (Mensajeria.id_receptor == id_receptor)) |
        ((Mensajeria.id_emisor == id_receptor) & (Mensajeria.id_receptor == id_emisor))
    ).order_by(Mensajeria.fecha.asc()).all()

    resultado = [
        {
            'mensaje_id': m.mensaje_id,
            'id_emisor': m.id_emisor,
            'id_receptor': m.id_receptor,
            'texto': m.texto,
            'fecha': m.fecha.strftime('%Y-%m-%d %H:%M:%S')
        } for m in mensajes
    ]

    return jsonify(resultado), 200

@mensajeria_bp.route('/usuarios', methods=['GET'])
@login_required
def obtener_usuarios():
    usuarios = Usuario.query.filter(Usuario.usuario_id != current_user.usuario_id).all()

    resultados = []
    for user in usuarios:
        perfil = perfiles.query.filter_by(id_usuario=user.usuario_id).first()

        nombre = (f"{perfil.primer_nombre or ''} {perfil.primer_apellido or ''}".strip()
                  if perfil and perfil.primer_nombre else user.correo.split('@')[0])
        foto = perfil.foto_perfil if perfil and perfil.foto_perfil else 'default.jpg'

        resultados.append({
            "usuario_id": user.usuario_id,
            "correo": user.correo,
            "nombre": nombre,
            "foto": foto
        })

    return jsonify(resultados)
