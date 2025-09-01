from app.extensions import db

class Guardados(db.Model):
    __tablename__ = 'guardados'

    guardado_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete="CASCADE"), nullable=False)
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicaciones.publicacion_id', ondelete="CASCADE"), nullable=False)
    fecha_guardado = db.Column(db.DateTime, server_default=db.text('current_timestamp'))

    # Relaciones (opcional, para acceso fácil)
    usuario = db.relationship('Usuario', back_populates='guardados')
    publicacion = db.relationship('Publicaciones')

    def __repr__(self):
        return f"<Guardado usuario={self.usuario_id} publicacion={self.publicacion_id}>"


    def to_dict(self):
        return {
            "guardado_id": self.guardado_id,
            "usuario_id": self.usuario_id,
            "publicacion_id": self.publicacion_id,
            "fecha_guardado": self.fecha_guardado.isoformat() if self.fecha_guardado else None,
            "publicacion": self.publicacion.to_dict() if self.publicacion else None
        }