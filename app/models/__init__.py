# /app/models/__init__.py
from .usuario import Usuario
from .perfiles import Perfiles
from .roles import Roles
from .mensajeria import Mensajeria
from .publicaciones import Publicaciones
from .reseñas import Reseñas
from .aptitudes import Aptitudes
from .categorias import Categorias
from .estudios import Estudios
from .experiencias import Experiencias
from .idiomas import Idiomas
from .perfil_idioma import perfil_idioma
from .subcategorias import Subcategorias
from app.extensions import db

Usuario.mensajes_enviados = db.relationship(
    'Mensajeria',
    foreign_keys=[Mensajeria.id_emisor],
    back_populates='emisor',
    cascade='all, delete-orphan'
)

Usuario.mensajes_recibidos = db.relationship(
    'Mensajeria',
    foreign_keys=[Mensajeria.id_receptor],
    back_populates='receptor',
    cascade='all, delete-orphan'
)

Mensajeria.emisor = db.relationship(
    'Usuario',
    foreign_keys=[Mensajeria.id_emisor],
    back_populates='mensajes_enviados'
)

Mensajeria.receptor = db.relationship(
    'Usuario',
    foreign_keys=[Mensajeria.id_receptor],
    back_populates='mensajes_recibidos'
)
