# app/services/mensajeria.py

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from datetime import datetime

from app.extensions import db, socketio
from app.models.mensajeria import Mensajeria
from app.models.usuario import Usuario
from app.models.perfiles import perfiles

mensajeria_bp = Blueprint('mensajeria', __name__, url_prefix='/mensajeria')


# ─── RUTAS HTTP ──────────────────────────────────────────────────────────────

@mensajeria_bp.route('/')
@login_required
def mensajeria():
    return render_template('mensajeria.html')

def _room_name(a, b):
    return f"chat_{min(a, b)}_{max(a, b)}"


@mensajeria_bp.route('/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json() or {}
    id_emisor   = data.get('id_emisor')
    id_receptor = data.get('id_receptor')
    texto       = data.get('texto', '').strip()

    if not id_emisor or not id_receptor or not texto:
        return jsonify({'error': 'Faltan campos requeridos.'}), 400

    try:
        id_emisor   = int(id_emisor)
        id_receptor = int(id_receptor)
    except ValueError:
        return jsonify({'error': 'IDs inválidos.'}), 400

    mensaje = Mensajeria(
        id_emisor   = id_emisor,
        id_receptor = id_receptor,
        texto       = texto,
        fecha       = datetime.utcnow()
    )
    db.session.add(mensaje)
    db.session.commit()

    return jsonify({'message': 'Mensaje enviado correctamente.'}), 201


@mensajeria_bp.route('/conversaciones/<int:usuario_id>', methods=['GET'])
def obtener_conversaciones(usuario_id):
    mensajes = Mensajeria.query.filter(
        (Mensajeria.id_emisor   == usuario_id) |
        (Mensajeria.id_receptor == usuario_id)
    ).order_by(Mensajeria.fecha.desc()).all()

    


    contactos = {}
    for m in mensajes:
        otro_id = m.id_receptor if m.id_emisor == usuario_id else m.id_emisor
        if otro_id not in contactos:
            u      = Usuario.query.get(otro_id)
            perfil = perfiles.query.filter_by(id_usuario=otro_id).first()

            nombre = (
                f"{perfil.primer_nombre or ''} {perfil.primer_apellido or ''}".strip()
                if perfil and perfil.primer_nombre
                else u.correo.split('@')[0]
            )
            foto = perfil.foto_perfil if perfil and perfil.foto_perfil else 'default.jpg'
            
            pendientes = Mensajeria.query.filter_by(
                id_emisor=otro_id,
                id_receptor=usuario_id,
                leido=False
            ).count()

            contactos[otro_id] = {
                'usuario_id':     u.usuario_id,
                'correo':         u.correo,
                'nombre':         nombre,
                'foto':           foto,
                'ultimo_mensaje': m.texto,
                'fecha':          m.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'pendientes': pendientes
            }

    return jsonify(list(contactos.values())), 200


@mensajeria_bp.route('/<int:id_emisor>/<int:id_receptor>', methods=['GET'])
def obtener_mensajes(id_emisor, id_receptor):
    historial = Mensajeria.query.filter(
        ((Mensajeria.id_emisor   == id_emisor)   & (Mensajeria.id_receptor == id_receptor)) |
        ((Mensajeria.id_emisor   == id_receptor) & (Mensajeria.id_receptor == id_emisor))
    ).order_by(Mensajeria.fecha.asc()).all()

    resultado = [
        {
            'mensaje_id':  m.mensaje_id,
            'id_emisor':   m.id_emisor,
            'id_receptor': m.id_receptor,
            'texto':       m.texto,
            'fecha':       m.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'leido':       getattr(m, 'leido', False)
        }
        for m in historial
    ]

    return jsonify(resultado), 200


@mensajeria_bp.route('/usuarios', methods=['GET'])
@login_required
def obtener_usuarios():
    usuarios = Usuario.query.filter(Usuario.usuario_id != current_user.usuario_id).all()
    resultados = []

    for u in usuarios:
        perfil = perfiles.query.filter_by(id_usuario=u.usuario_id).first()
        nombre = (
            f"{perfil.primer_nombre or ''} {perfil.primer_apellido or ''}".strip()
            if perfil and perfil.primer_nombre
            else u.correo.split('@')[0]
        )
        foto = perfil.foto_perfil if perfil and perfil.foto_perfil else 'default.jpg'
        resultados.append({
            'usuario_id': u.usuario_id,
            'correo':     u.correo,
            'nombre':     nombre,
            'foto':       foto
        })

    return jsonify(resultados), 200


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def _room_name(a, b):
    """
    Construye un nombre de sala único para dos usuarios,
    forzando ambos IDs a entero para evitar TypeError.
    """
    try:
        a_int = int(a)
        b_int = int(b)
    except (TypeError, ValueError):
        return None

    a_int, b_int = sorted([a_int, b_int])
    return f"chat_{a_int}_{b_int}"


# ─── SOCKET.IO ────────────────────────────────────────────────────────────────

@socketio.on('join_chat')
def handle_join(data):
    print("🔌 SID que se une:", request.sid)

    print("🔥 server recibió join_chat:", data)

    try:
        user_id = int(data.get('user_id'))
        other_id = int(data.get('other_user_id'))
    except (TypeError, ValueError):
        return

    room = _room_name(user_id, other_id)
    join_room(room)

    historial = Mensajeria.query.filter(
        ((Mensajeria.id_emisor == user_id) & (Mensajeria.id_receptor == other_id)) |
        ((Mensajeria.id_emisor == other_id) & (Mensajeria.id_receptor == user_id))
    ).order_by(Mensajeria.fecha.asc()).all()

    mensajes_pendientes = [
        m for m in historial if m.id_receptor == user_id and not getattr(m, 'leido', False)
    ]
    if mensajes_pendientes:
        for m in mensajes_pendientes:
            m.leido = True
        db.session.commit()

        ids = [m.mensaje_id for m in mensajes_pendientes]
        emit('message_read', {'mensaje_id': ids}, room=_room_name(user_id, other_id))
        
        # Avisar solo al otro usuario que refresque su lista
        sid_otro = obtener_sid_usuario(other_id)  # tu función para mapear user_id → sid
        if sid_otro:
            emit('update_conversations', {}, to=sid_otro)

    emit('chat_history', [m.to_dict() for m in historial], to=request.sid)





@socketio.on('send_message')
def handle_send(data):
    print("🔥 servidor recibió send_message:", data)

    mensaje = Mensajeria(
        id_emisor   = data['user_id'],
        id_receptor = data['other_user_id'],
        texto       = data['texto']
    )
    db.session.add(mensaje)
    db.session.commit()

    payload = mensaje.to_dict()
    room = _room_name(mensaje.id_emisor, mensaje.id_receptor)

    join_room(room)  # Asegura que el emisor esté en la sala
    emit('new_message', payload, room=room)
    print("🔥 servidor emitió new_message a room:", room, "con payload:", payload)

@socketio.on('message_seen')
def handle_seen(data):
    mensaje_id = data.get('mensaje_id')
    user_id    = data.get('user_id')

    mensaje = Mensajeria.query.get(mensaje_id)
    if mensaje and mensaje.id_receptor == user_id and not mensaje.leido:
        mensaje.leido = True
        db.session.commit()

        # Avisar con ✔✔ al emisor
        emit('message_read', {'mensaje_id': mensaje_id}, room=_room_name(mensaje.id_emisor, mensaje.id_receptor))

        # 🔔 Avisar solo al emisor que refresque su lista
        sid_emisor = _obtener_sid_de_usuario(mensaje.id_emisor)  # tu propia forma de mapear user_id→SID
        if sid_emisor:
            emit('update_conversations', {}, to=sid_emisor)




@socketio.on('typing')
def handle_typing(data):
    user_id  = data.get('user_id')
    other_id = data.get('other_user_id')
    room = _room_name(user_id, other_id)
    if room:
        emit('user_typing', data, room=room)


@socketio.on('stop_typing')
def handle_stop_typing(data):
    user_id  = data.get('user_id')
    other_id = data.get('other_user_id')
    room = _room_name(user_id, other_id)
    if room:
        emit('stop_typing', data, room=room)
