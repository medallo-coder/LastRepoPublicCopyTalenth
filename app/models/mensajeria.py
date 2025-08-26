from app.extensions import db
from datetime       import datetime

class Mensajeria(db.Model):
    __tablename__ = 'mensajeria'

    mensaje_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_emisor   = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete='CASCADE'))
    id_receptor = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete='CASCADE'))
    texto       = db.Column(db.Text, nullable=False)
    fecha       = db.Column(db.DateTime, default=datetime.utcnow)
    leido       = db.Column(db.Boolean, default=False, nullable=False)   # ← nuevo

    emisor   = db.relationship('Usuario', foreign_keys=[id_emisor])
    receptor = db.relationship('Usuario', foreign_keys=[id_receptor])

    def to_dict(self):
        return {
            'mensaje_id': self.mensaje_id,
            'emisor':     self.emisor.usuario_id,
            'receptor':   self.receptor.usuario_id,
            'texto':      self.texto,
            'fecha':      self.fecha.isoformat(),
            'leido':      self.leido
        }
