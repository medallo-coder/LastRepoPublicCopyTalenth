from app.extensions import db

class Publicaciones(db.Model):
    __tablename__ = 'publicaciones'

    publicacion_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id', ondelete="CASCADE"), nullable=False)
    fecha = db.Column(db.DateTime, server_default=db.text('current_timestamp'))
    titulo = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.categoria_id', ondelete="CASCADE"), nullable=True)
    subcategoria_id = db.Column(db.Integer, db.ForeignKey('subcategorias.subcategoria_id', ondelete="SET NULL"), nullable=True)
    descripcion_publicacion = db.Column(db.String(200), nullable=True)
    destacada = db.Column(db.String(2), nullable=False, default="no", server_default="no")
    cantidad = db.Column(db.Integer, default= 0)
    estado = db.Column(db.String(200), nullable=True)



    categoria = db.relationship('Categorias', back_populates='publicaciones', passive_deletes=True)
    subcategoria = db.relationship('Subcategorias', back_populates='publicaciones', passive_deletes=True)
    usuario = db.relationship('Usuario', back_populates='publicaciones', passive_deletes=True)
    

    def __repr__(self):
        return f"<Publicacion {self.publicacion_id}>"
