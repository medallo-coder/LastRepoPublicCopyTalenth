from app.extensions import db

class Categorias(db.Model):
    __tablename__ = 'categorias'

    categoria_id = db.Column(db.Integer,primary_key=True, autoincrement=True, nullable=False) 
    tipo_categoria = db.Column(db.String(100), nullable=False)

    
    publicaciones = db.relationship('Publicaciones', back_populates='categoria', passive_deletes=True)
    subcategorias = db.relationship('Subcategorias', back_populates='categoria', passive_deletes=True)

    def __repr__(self):
        return f"<Categoria {self.tipo_categoria}>"




