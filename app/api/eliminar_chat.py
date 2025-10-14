import requests
from flet import Page

def eliminar_chat_api(token: str, otro_usuario_id: int):
    """
    Envía la petición DELETE al backend para eliminar el chat.
    Utiliza el Token JWT para la autenticación.
    """
    url = f"http://127.0.0.1:5000/mensajeria/eliminar_chat/{otro_usuario_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",  # CLAVE: Token para autenticar en móvil
        "Content-Type": "application/json"
    }

    try:
        # Petición DELETE
        response = requests.delete(url, headers=headers, timeout=10)
        
        # El backend debe devolver 200 OK
        if response.status_code == 200:
            return {"success": True, "message": "Conversación eliminada con éxito."}
        
        # Manejo de errores 400 (Bad Request), 401 (Unauthorized), etc.
        try:
            data = response.json()
            return {"success": False, "message": data.get("mensaje", "Error desconocido del servidor.")}
        except requests.JSONDecodeError:
            return {"success": False, "message": f"Error {response.status_code}: No se pudo procesar la respuesta."}

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al eliminar chat: {e}")
        return {"success": False, "message": "Error de conexión o timeout."}