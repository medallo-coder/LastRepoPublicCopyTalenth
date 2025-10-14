from flask import Blueprint, jsonify
from app.services_movil.mensajeria import obtener_conversaciones_service
from app.models.mensajeria import Mensajeria

mensajeria_movil_bp = Blueprint('mensajeria_movil', __name__)

@mensajeria_movil_bp.route('/movil/conversaciones/<int:usuario_id>', methods=['GET'])
def obtener_conversaciones(usuario_id):
    conversaciones = obtener_conversaciones_service(usuario_id)
    return jsonify(conversaciones)

@mensajeria_movil_bp.route("/api/conversacion/existe/<int:user_id>/<int:receptor_id>", methods=["GET"])
def verificar_conversacion(user_id, receptor_id):
    try:
        # Busca si ya hay mensajes entre ambos usuarios (en cualquier dirección)
        chat = db.session.query(Mensajeria).filter(
            ((Mensajeria.id_emisor == user_id) & (Mensajeria.id_receptor == receptor_id)) |
            ((Mensajeria.id_emisor == receptor_id) & (Mensajeria.id_receptor == user_id))
        ).first()

        if chat:
            return jsonify({"existe": True})
        else:
            return jsonify({"existe": False})
    except Exception as e:
        print("❌ Error verificando conversación:", e)
        return jsonify({"error": str(e)}), 500
