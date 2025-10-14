from app.extensions import db

## @brief Modelo que representa las aptitudes de un perfil dentro del sistema.
class Aptitudes(db.Model):
    __tablename__ = 'aptitudes'
   
    aptitud_id = db.Column(db.Integer, primary_key=True)
    ## Identificador único de la aptitud.
    id_perfil = db.Column(db.Integer, db.ForeignKey('perfiles.id_perfil', ondelete="CASCADE"), nullable=False)
    tipo_aptitud = db.Column(db.String(255))

    perfiles =  db.relationship('perfiles', back_populates='aptitudes', passive_deletes=True)
    ## Relación inversa con la tabla de perfiles.

    ## @brief Representación en texto del objeto Aptitudes.
    #  @return Cadena con el tipo de aptitud.
    def __repr__(self):
        return f"<Aptitud {self.tipo_aptitud}>"