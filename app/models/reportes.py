from app.extensions import db


class Reportes(db.Model):
    __tablename__= 'reportes'

    reporte_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False )
    descripcion_reporte= db.Column(db.Text, nullable=True)
    fecha_reporte= db.Column(db.Date)
    reportador_id= db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete="CASCADE"), nullable=False)
    reportado_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete="CASCADE"), nullable=False)


    reportador = db.relationship('Usuario', foreign_keys='Reportes.reportador_id', back_populates='reportes_hechos')
    asignado = db.relationship('Usuario', foreign_keys='Reportes.reportado_id', back_populates='reportes_asignados')




    def __repr__(self):
        print(f"Reporte {self.reporte_id}")


