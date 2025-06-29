from app.extensions import db
from app.models.perfil_idioma import perfil_idioma


class Perfiles(db.Model):
    __tablename__ = 'perfiles'
   
    id_perfil = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete="CASCADE"), nullable=False)
    primer_nombre = db.Column(db.String(100), nullable=False)
    primer_apellido = db.Column(db.String(100), nullable=False)
    segundo_nombre = db.Column(db.String(100), nullable=True)
    segundo_apellido = db.Column(db.String(100), nullable=True)
    especialidad = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.Text, nullable=True)
    foto_perfil = db.Column(db.String(255), nullable=True)
    descripcion_perfil = db.Column(db.Text, nullable=True)

    usuario = db.relationship('Usuario', back_populates='perfiles',passive_deletes=True)
    idioma = db.relationship('Idiomas', secondary= perfil_idioma, back_populates='perfiles',passive_deletes=True)
    aptitudes = db.relationship('Aptitudes', back_populates='perfiles',passive_deletes=True)
    estudios = db.relationship('Estudios', back_populates='perfil',passive_deletes=True)
    experiencias = db.relationship('Experiencias', back_populates='perfil',passive_deletes=True)

    def __repr__(self):
        return f"<Perfiles(id_perfil={self.id_perfil}')>"