import mercadopago
import os
from dotenv import load_dotenv

# Cargar las variables del .env
load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")  # Usamos el token del vendedor

sdk = mercadopago.SDK(ACCESS_TOKEN)

def crear_preferencia_pago(titulo, precio, cantidad, email_comprador):
    preference_data = {
        "items": [
            {
                "title": titulo,
                "quantity": cantidad,
                "currency_id": "COP",
                "unit_price": float(precio)
            }
        ],
        "payer": {
            "email": email_comprador  # Email del comprador
        },
        "back_urls": {
            "success": "https://www.tusitio.com/pago-exitoso",
            "failure": "https://www.tusitio.com/pago-fallido",
            "pending": "https://www.tusitio.com/pago-pendiente"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    return preference_response["response"]["init_point"]
