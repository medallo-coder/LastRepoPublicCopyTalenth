from app import create_app

# Crear la instancia de la aplicación
app = create_app()

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)  # Cambia debug=True si deseas habilitar la depuración

from flask import Blueprint, render_template, session

main = Blueprint('main', __name__)

