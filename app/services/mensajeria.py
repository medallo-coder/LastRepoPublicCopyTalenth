# app/services/mensajeria.py

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from datetime import datetime
from sqlalchemy import or_, func, case
from flask import redirect, url_for, session

from app.extensions import db, socketio
from app.models.mensajeria import Mensajeria
from app.models.usuario import Usuario
from app.models.perfiles import perfiles

from datetime import datetime, date
from flask import flash
from app.models.calificaciones import Calificaciones


mensajeria_bp = Blueprint('mensajeria', __name__, url_prefix='/mensajeria')

user_sid_map = {}  # Guarda: user_id → socket.id

# ─── RUTAS HTTP ──────────────────────────────────────────────────────────────

@mensajeria_bp.route('/')
@login_required
def mensajeria():

    calificador_id = current_user.usuario_id
    calificado_id = session.get('abrir_chat_con')  # puede ser None si no hay chat abierto

    return render_template(
        'mensajeria.html',
        calificador_id=calificador_id,
        calificado_id=calificado_id,
        rol_usuario=current_user.id_rol
    )

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


from sqlalchemy import case

@mensajeria_bp.route('/conversaciones/<int:usuario_id>', methods=['GET'])
def obtener_conversaciones(usuario_id):
    try:
        mensajes = Mensajeria.query.filter(
            or_(
                Mensajeria.id_emisor == usuario_id,
                Mensajeria.id_receptor == usuario_id
            )
        ).order_by(Mensajeria.fecha.desc()).all()

        conversaciones = {}

        for m in mensajes:
            otro_id = m.id_receptor if m.id_emisor == usuario_id else m.id_emisor
            if otro_id not in conversaciones:
                conversaciones[otro_id] = {
                    'ultimo_texto': m.texto,
                    'hora': m.fecha.strftime('%H:%M'),
                    'pendientes': 0,
                    'fecha': m.fecha
                }
            if m.id_receptor == usuario_id and not m.leido:
                conversaciones[otro_id]['pendientes'] += 1

        resultado = []
        for otro_id, datos in conversaciones.items():
            usuario = Usuario.query.get(otro_id)
            if not usuario:
                continue
            perfil = perfiles.query.filter_by(id_usuario=usuario.usuario_id).first()
            nombre = (
                f"{perfil.primer_nombre or ''} {perfil.primer_apellido or ''}".strip()
                if perfil and perfil.primer_nombre
                else usuario.correo.split('@')[0]
            )
            foto = perfil.foto_perfil if perfil and perfil.foto_perfil else 'default.jpg'

            resultado.append({
                'usuario_id': usuario.usuario_id,
                'correo': usuario.correo,
                'nombre': nombre,
                'foto': foto,
                'ultimo_texto': datos['ultimo_texto'],
                'hora': datos['hora'],
                'pendientes': datos['pendientes']
            })

        # Ordenar por fecha del último mensaje
        resultado.sort(key=lambda x: x['hora'], reverse=True)

        return jsonify(resultado), 200

    except Exception as e:
        print("❌ Error en obtener_conversaciones:", e)
        return jsonify({'error': 'Error interno en conversaciones'}), 500


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

def _obtener_sid_de_usuario(user_id):
    return user_sid_map.get(int(user_id))



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
        sid_otro = _obtener_sid_de_usuario(other_id)  # tu función para mapear user_id → sid
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
    # 🔔 Notificar al receptor que hay un nuevo mensaje y debe refrescar la lista
    sid_receptor = _obtener_sid_de_usuario(mensaje.id_receptor)
    if sid_receptor:
        emit('update_conversations', {}, to=sid_receptor)


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

@socketio.on('identify')
def identify_user(data):
    user_id = data.get('user_id')
    if user_id:
        user_sid_map[int(user_id)] = request.sid
        print(f"✅ Usuario {user_id} identificado con SID {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    # Eliminar cualquier mapeo que use este SID
    for uid, sid in list(user_sid_map.items()):
        if sid == request.sid:
            print(f"🔌 Usuario {uid} desconectado")
            del user_sid_map[uid]
            break

@mensajeria_bp.route('/iniciar_chat/<int:experto_id>', methods=['POST'])
@login_required
def iniciar_chat_con_experto(experto_id):
    print(f"📨 Contacto iniciado con el experto {experto_id}")

    if experto_id == current_user.usuario_id:
        return redirect(url_for('mensajeria.mensajeria'))

    # Crea mensaje automático
    mensaje = Mensajeria(
        id_emisor=current_user.usuario_id,
        id_receptor=experto_id,
        texto="Hola, estoy interesado en tus servicios",
        fecha=datetime.utcnow()
    )
    db.session.add(mensaje)
    db.session.commit()

    session['abrir_chat_con'] = experto_id  # 🔥 marca para abrir al renderizar mensajeria.html
    return redirect(url_for('mensajeria.mensajeria'))


@mensajeria_bp.route('/guardar_calificacion', methods=['POST'])
@login_required
def guardar_calificacion():
    try:
        calificador_id = request.form.get('calificador_id')
        calificado_id = request.form.get('calificado_id')
        reseña = request.form.get('reseña')
        puntaje = request.form.get('valor_calificacion')

        print(f"💾 DATOS RECIBIDOS: {calificador_id}, {calificado_id}, {reseña}, {puntaje}")

        # Validar datos
        if not calificador_id or not calificado_id or not reseña or not puntaje:
            flash("Faltan datos en la calificación", "error")
            return redirect(url_for('mensajeria.mensajeria'))

        # Guardar en la base de datos
        nueva_calificacion = Calificaciones(
            reseña=reseña,
            puntaje=puntaje,
            fecha_calificacion=date.today(),
            calificador_id=calificador_id,
            calificado_id=calificado_id
        )
        db.session.add(nueva_calificacion)
        db.session.commit()

        flash("✅ Calificación enviada correctamente", "success")
        return redirect(url_for('mensajeria.mensajeria'))

    except Exception as e:
        db.session.rollback()
        print("❌ Error al guardar calificación:", e)
        flash("Error al guardar calificación: " + str(e), "error")
        return redirect(url_for('mensajeria.mensajeria'))

