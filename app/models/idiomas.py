from app.extensions import db
from app.models.perfil_idioma import perfil_idioma


class Idiomas(db.Model):
    __tablename__ = 'idiomas'
    
    idioma_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre_idioma = db.Column(db.String(50), nullable=False)

    perfiles = db.relationship('Perfiles', secondary= perfil_idioma, back_populates='idioma', passive_deletes=True)

    def __repr__(self):
        return f"<Idioma {self.nombre_idioma}>"
    



