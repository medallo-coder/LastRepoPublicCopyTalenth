from app.extensions import db

class Roles(db.Model):
    __tablename__ = 'roles'

    id_rol  = db.Column(db.Integer, primary_key=True)
    tipo_rol = db.Column(db.String(50), nullable=False, unique=True)

    usuarios = db.relationship('Usuario', back_populates='rol')

    def __repr__(self):
        return f"<Role {self.tipo_rol}>"




