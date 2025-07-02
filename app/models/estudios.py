from app.extensions import db


class Estudios(db.Model):
    __tablename__ = 'estudios'
    

    id_estudio = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    institucion = db.Column(db.String(255), nullable=False)
    titulo_obtenido = db.Column(db.String(255), nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin  =  db.Column(db.Date)
    nivel_educativo= db.Column(db.String(100), nullable=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey('perfiles.id_perfil', ondelete="CASCADE"), nullable=False)
   
    
    perfil = db.relationship('perfiles', back_populates='estudios', passive_deletes=True)
    
    def __repr__(self):
        return f"<Estudio {self.id_estudio}>"