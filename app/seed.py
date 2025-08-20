from app.extensions import db
from app.models.categorias import Categorias
from app.models.idiomas import Idiomas
from app.models.roles import Roles
from app.models.subcategorias import Subcategorias
from app  import create_app



def añadir_categorias():
    categorias = [
        "Reparación y Mantenimiento",
        "Cuidado y Asistencia",
        "Bienestar de Mascotas",
        "Educativos y aprendizaje",
        "Hogar y Limpieza",
        "Construcción y Remodelación",
        "Artísticos y creatividad visual",
        "Movilidad y transporte",
        "Gastronomía",
        "Eventos",
        "Bienestar Personal"
    ]

    for tipo in categorias:
        if not Categorias.query.filter_by(tipo_categoria=tipo).first():
            db.session.add(Categorias(tipo_categoria=tipo))

    db.session.commit()
    print("Categorías insertadas correctamente.")

def añadir_idiomas():
    idiomas = [
        "Español",
        "Ingles",
        "Frances",
        "Aleman",
        "Portugués"
    ]

    for tipo in idiomas:
        if not Idiomas.query.filter_by(nombre_idioma=tipo).first():
            db.session.add(Idiomas(nombre_idioma=tipo))
    
    db.session.commit()
    print("Idiomas insertadas correctamente.")

def añadir_roles():
    roles= [
        "experto",
        "cliente",
        "admin"
    ]

    for tipo in roles:
        if not Roles.query.filter_by(tipo_rol=tipo).first():
            db.session.add(Roles(tipo_rol=tipo))
    
    db.session.commit()
    print("Roles insertados correctamente.")


def añadir_subcategorias():

    

    subcategorias={
        1: [
            "Plomería",
            "Electricidad",
            "Carpintería",
            "Pintura y decoración",
            "Reparaciones generales",
            "Cerrajería",
            "Reparación de electrodomésticos",
            "Técnico en computadoras / celulares"
        ],

        2: [
            "Cuidado de adultos mayores",
            "Cuidado de niños / niñera",
            "Asistencia personal"
        ],
        3: [
            "Cuidado de mascotas",
            "Paseo de mascotas",
            "Guardería y baño para mascotas"
        ],
        4: [
            "Clases particulares",
            "Coaching",
            "Enseñanza de idiomas",
            "Formación en habilidades digitales",
            "Clases de música",
            "Tutorías"
        ],
        5: [
            "Aseo doméstico",
            "Jardinería y poda",
            "Organización de espacios",
            "Desinfección y sanitización",
            "Lavado de alfombras y tapicería",
            "Fumigación"
        ],
        6: [
            "Albañilería",
            "Instalación de pisos",
            "Remodelación de cocinas y baños",
            "Reparación de techos",
            "Diseño de interiores",
            "Impermeabilización"
        ],
        7: [
            "Fotografía y edición",
            "Redacción y traducción de textos",
            "Producción y edición de video",
            "Diseño gráfico"
        ],
        8: [
            "Mudanzas",
            "Reparto / domicilios locales",
            "Transporte escolar",
            "Transporte para mascotas",
            "Alquiler de vehículo con conductor"
        ],
        9: [
            "Repostería personalizada",
            "Chef a domicilio",
            "Menús especiales"
        ],
        10: [
            "Organización de eventos sociales",
            "Decoración para fiestas",
            "Alquiler de mobiliario y sonido"
        ],
        11: [
            "Entrenador/a personal",
            "Masajes terapéuticos y relajantes",
            "Estética",
            "Yoga y meditación"
        ]
    }
     
    for categoria_id, lista_subs in subcategorias.items():
        for nombre_sub in lista_subs:
            existe = Subcategorias.query.filter_by(nombre_subcategoria=nombre_sub, categoria_id=categoria_id).first()
            if not existe:
                 db.session.add(Subcategorias(nombre_subcategoria=nombre_sub, categoria_id=categoria_id))

    db.session.commit()
    print("Subcategorias  insertadas correctamente.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        añadir_categorias()
        añadir_idiomas()
        añadir_roles()
        añadir_subcategorias()