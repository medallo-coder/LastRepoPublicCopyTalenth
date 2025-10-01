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

    def to_dict(self):
        return {
            "publicacion_id": self.publicacion_id,
            "usuario_id": self.usuario_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "nombre": self.usuario.perfiles.primer_nombre.capitalize(),
            "nombre_experto": self.usuario.perfiles.primer_nombre.capitalize() if self.usuario else None,
            "costo": float(self.precio) if self.precio is not None else None,
            "descripcion": self.descripcion_publicacion,
            "categoria": self.categoria.tipo_categoria if self.categoria else None,
            "calificacion":4,
            "subcategoria": self.subcategoria.nombre_subcategoria if self.subcategoria else None,
            "foto_perfil": self.usuario.perfiles.foto_perfil
         }
