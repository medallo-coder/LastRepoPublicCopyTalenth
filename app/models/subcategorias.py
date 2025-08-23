from app.extensions import db

class Subcategorias(db.Model):
    __tablename__ = 'subcategorias'

    subcategoria_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre_subcategoria = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.categoria_id', ondelete="CASCADE"), nullable=False)

    categoria = db.relationship('Categorias', back_populates='subcategorias', passive_deletes=True)
    publicaciones = db.relationship('Publicaciones', back_populates='subcategoria', passive_deletes=True)

    def __repr__(self):
        return f"<Subcategoria {self.nombre_subcategoria}>"
