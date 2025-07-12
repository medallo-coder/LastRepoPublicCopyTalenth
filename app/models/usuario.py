from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class Usuario(db.Model, UserMixin):  #Hereda de UserMixin (mensajeria)
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    correo = db.Column(db.String(50), unique=True, nullable=False)
    estado = db.Column(db.String(20), default='activo')
    intentos_fallidos = db.Column(db.Integer, default=0)
    bloqueado_hasta = db.Column(db.DateTime, nullable=True) 
    token_recuperacion = db.Column(db.String(255), nullable=True)

    id_rol  = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False, default=2)  
    
    rol = db.relationship('Roles', back_populates='usuarios')
    
    perfiles = db.relationship('perfiles', back_populates='usuario', uselist=False, passive_deletes=True)
    publicaciones = db.relationship('Publicaciones', back_populates='usuario', passive_deletes=True)
    reseñas = db.relationship('Reseñas', back_populates='usuario', passive_deletes=True)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False, default=2)  

    rol = db.relationship('Roles', back_populates='usuarios')

    perfiles = db.relationship('perfiles', back_populates='usuario', uselist=False)
    publicaciones = db.relationship('Publicaciones', back_populates='usuario')
    reseñas = db.relationship('Reseñas', back_populates='usuario')
    guardados = db.relationship('Guardados', back_populates='usuario', passive_deletes=True)


    #se añadio la funcion is_active y get_id (mensajeria)
    def is_active(self):
        return True  # Usuario siempre activo

    def get_id(self):
        return str(self.usuario_id)  # Devuelve el ID del usuario


    def __repr__(self):
        return f"<Usuario {self.correo}>"

    def set_password(self, password):
        """Genera el hash de la contraseña y lo guarda."""
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return check_password_hash(self.contrasena, password)
