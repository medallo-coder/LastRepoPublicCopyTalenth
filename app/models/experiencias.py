from app.extensions import db


class Experiencias(db.Model):
    __tablename__ = 'experiencias'
  

    id_experiencia = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_perfil= db.Column(db.Integer, db.ForeignKey('perfiles.id_perfil', ondelete="CASCADE"), nullable= False)
    nombre= db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_inicio_experiencia = db.Column(db.Date, nullable=True)
    fecha_fin_experiencia = db.Column(db.Date, nullable=True)

    perfil = db.relationship('perfiles', back_populates='experiencias', passive_deletes=True)
    
    def __repr__(self):
        return f"<Experiencia {self.id_experiencia}>"
    
