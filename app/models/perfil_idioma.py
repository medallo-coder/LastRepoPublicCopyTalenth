from app.extensions import db


perfil_idioma = db.Table(
    'perfil_idioma',
    db.Column('id_perfil', db.Integer, db.ForeignKey('perfiles.id_perfil', ondelete='CASCADE' ),  primary_key=True, nullable=False),
    db.Column('idioma_id', db.Integer, db.ForeignKey('idiomas.idioma_id', ondelete='CASCADE'),  primary_key=True, nullable=False),

)