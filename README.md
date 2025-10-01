#  CaliTrabaja – Documentación técnica


Bienvenido a la documentación técnica del **proyecto CaliTrabaja**.  
Este sistema fue desarrollado como una plataforma que conecte de forma segura y
eficiente a clientes y expertos, impulsando el desarrollo local., con versiones para **web, escritorio y móvil**.

---

## 🎯 Objetivo
El proyecto tiene como objetivo principal:
- Interfaz intuitiva y multiplataforma.
- Sistema de calificaciones y reportes.
- Seguridad, escalabilidad y estabilidad.


---

## ⚙️ Tecnologías usadas
- **Backend**
  - Python 3.11
  - Flask (servidor principal)
  - FastAPI (API adicional y documentación interactiva)
  - MySQL (base de datos relacional)

- **Frontend**
  - Jinja2 (Motor de plantillas de flask) para web 
  - Flet (Python) para aplicaciones móviles
  - Flet (Python) para aplicación de escritorio

---

## 🔑 Funcionalidades
- ✅ **CRUD de usuarios y datos básicos**  
  (crear, leer, actualizar, eliminar registros)
- ✅ Conexión a base de datos MySQL
- ✅ Aplicación multiplataforma (móvil y escritorio con Flet)
- ✅ API documentada con FastAPI
- ✅ Interfaz de usuario intuitiva

---

## 🚀 Ejecución del proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/usuario/CaliTrabaja.git
cd CaliTrabaja

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv .venv
.\.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
- Crear una base de datos en MySQL
- Ajustar credenciales en el archivo de configuración del proyecto

# 5. Levantar el servidor Flask
flask run
