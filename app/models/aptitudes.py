from app.extensions import db

class Aptitudes(db.Model):
    __tablename__ = 'aptitudes'
   

    aptitud_id = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey('perfiles.id_perfil', ondelete="CASCADE"), nullable=False)
    tipo_aptitud = db.Column(db.String(255))

    perfiles =  db.relationship('Perfiles', back_populates='aptitudes', passive_deletes=True)
    
    def __repr__(self):
        return f"<Aptitud {self.tipo_aptitud}>"