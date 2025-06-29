# services/mensajeria.py
"""Este archivo se crea de forma temporal ya que solo se hizo con el fin de realizar pruebas mas adelante se pasa a la carpeta de sevice y se adapta el codigo"""

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.mensajeria import Mensajeria
from app.models.usuario import Usuario
from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user

mensajeria_bp = Blueprint('mensajeria', __name__, url_prefix='/mensajeria')

@mensajeria_bp.route('/')
@login_required
def mensajeria():
    print("Usuario actual en sesión:", current_user)
    return render_template('mensajeria.html', current_user=current_user)

# POST /mensajeria/enviar
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

# GET /mensajeria/conversaciones/<usuario_id>
@mensajeria_bp.route('/conversaciones/<int:usuario_id>', methods=['GET'])
def obtener_conversaciones(usuario_id):
    mensajes = Mensajeria.query.filter(
        (Mensajeria.id_emisor == usuario_id) | (Mensajeria.id_receptor == usuario_id)
    ).order_by(Mensajeria.fecha.desc()).all()

    if not mensajes:  # Si no hay mensajes, enviamos un array vacío
        return jsonify([]), 200
    
    contactos = {}
    for mensaje in mensajes:
        otro_usuario_id = mensaje.id_receptor if mensaje.id_emisor == usuario_id else mensaje.id_emisor
        if otro_usuario_id not in contactos:
            usuario = Usuario.query.get(otro_usuario_id)
            contactos[otro_usuario_id] = {
                'usuario_id': usuario.usuario_id,
                'correo': usuario.correo,
                'ultimo_mensaje': mensaje.texto,
                'fecha': mensaje.fecha.strftime('%Y-%m-%d %H:%M:%S')
            }

    return jsonify(list(contactos.values())), 200

# GET /mensajeria/<id_emisor>/<id_receptor>
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

    usuarios_json = [
        {"usuario_id": user.usuario_id, "correo": user.correo}
        for user in usuarios
    ]

    print("Usuarios disponibles:", usuarios_json)  # Debugging para ver si trae los datos correctamente
    return jsonify(usuarios_json)

