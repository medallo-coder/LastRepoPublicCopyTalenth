from app.extensions import db


class Mensajeria(db.Model):
    __tablename__ = 'mensajeria'
   

    mensaje_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_emisor = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete='CASCADE'), nullable=False)
    id_receptor  = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete='CASCADE'), nullable=False)
    texto= db.Column(db.Text, nullable=False)
    fecha= db.Column(db.DateTime, server_default=db.text('current_timestamp'))

   

    def __repr__(self):
        return f"<Mensajeria {self.mensaje_id}>"