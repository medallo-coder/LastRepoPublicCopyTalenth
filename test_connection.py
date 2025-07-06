from sqlalchemy import create_engine

# Configura aquí tu conexión (sin contraseña)
DATABASE_URI = 'mysql+pymysql://root:@localhost/dbejemplo'

try:
    # Crea un motor de conexión
    engine = create_engine(DATABASE_URI)
    
    # Intenta conectarse
    with engine.connect() as connection:
        print("✅ Conexión exitosa a la base de datos.")

except Exception as e:
    print("❌ Error al conectar a la base de datos.")
    print(f"Detalles del error: {e}")
