import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

GMAIL_CORREO = os.getenv('GMAIL_CORREO')
GMAIL_CONTRASENA_APP = os.getenv('GMAIL_CONTRASENA_APP')

# Enviar notificación de registro exitoso
def enviar_notificacion_registro(correo_destino, nombre_usuario):
    try:
        # Leer el contenido HTML desde el archivo
        
        with open('app/templates/EmailBienvenida.html', 'r', encoding='utf-8') as archivo:

            cuerpo_html = archivo.read()

        # Reemplazar marcador {nombre_usuario}
        cuerpo_html = cuerpo_html.replace('{nombre_usuario}', nombre_usuario)

        # Configurar servidor SMTP
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(GMAIL_CORREO, GMAIL_CONTRASENA_APP)

        # Crear el mensaje SOLO con lo necesario
        mensaje = MIMEMultipart()
        mensaje['From'] = GMAIL_CORREO
        mensaje['To'] = correo_destino
        mensaje['Subject'] = "Registro exitoso en ContrataHOY!"  # El asunto sigue siendo obligatorio

        # Adjuntar solo el HTML leído
        mensaje.attach(MIMEText(cuerpo_html, 'html'))

        # Enviar el correo
        servidor.send_message(mensaje)
        servidor.quit()

        return {"success": True, "message": "Correo de notificación enviado exitosamente."}
    
    except Exception as e:
        return {"success": False, "message": f"Error al enviar la notificación: {str(e)}"}








# Enviar enlace de recuperación de contraseña
def enviar_link_recuperacion_correo(correo_destino, nombre_usuario, link_recuperacion):
    try:
        # Leer la plantilla HTML
        with open('app/templates/link_recuperacion.html', 'r', encoding='utf-8') as archivo:
          cuerpo_html = archivo.read()

        # Reemplazar marcadores {nombre_usuario} y {link_recuperacion}
        cuerpo_html = cuerpo_html.replace('{nombre_usuario}', nombre_usuario)
        cuerpo_html = cuerpo_html.replace('{link_recuperacion}', link_recuperacion)

        # Configurar servidor SMTP
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(GMAIL_CORREO, GMAIL_CONTRASENA_APP)

        # Crear el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = GMAIL_CORREO
        mensaje['To'] = correo_destino
        mensaje['Subject'] = "Recupera tu contraseña en ContrataHOY"

        # Adjuntar el cuerpo del mensaje
        mensaje.attach(MIMEText(cuerpo_html, 'html'))

        # Enviar el correo
        servidor.send_message(mensaje)
        servidor.quit()

        return {"success": True, "message": "Correo de recuperación enviado exitosamente."}

    except Exception as e:
        return {"success": False, "message": f"Error al enviar el correo de recuperación: {str(e)}"}
