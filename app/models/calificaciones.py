from app.extensions import db

class Calificaciones(db.Model):
    __tablename__ = 'calificaciones'

    calificacion_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    reseña = db.Column(db.Text, nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    fecha_calificacion = db.Column(db.Date, nullable=False)
    calificador_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete="CASCADE"), nullable=False)
    calificado_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete="CASCADE"), nullable=False)

    calificador = db.relationship('Usuario', foreign_keys='Calificaciones.calificador_id', back_populates='calificaciones_hechas')
    calificado = db.relationship('Usuario', foreign_keys='Calificaciones.calificado_id', back_populates='calificaciones_asignadas')