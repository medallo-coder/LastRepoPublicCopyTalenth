from app.extensions import db

class Reseñas(db.Model):
    __tablename__ = 'reseñas'
   

    reseña_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete="CASCADE"), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='reseñas', passive_deletes=True)

    def __repr__(self):
        return f"<Reseñas {self.reseña_id}>"