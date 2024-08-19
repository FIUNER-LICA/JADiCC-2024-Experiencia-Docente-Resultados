from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
from config import app, db  # Asegúrate de que la configuración y la instancia de db están importadas correctamente

# Configurar el contexto de la aplicación
with app.app_context():
    # Conectar a la base de datos
    engine = db.engine
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Reflect the existing database
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Define the existing table
    reclamos = Table('TablaReclamos', metadata, autoload_with=engine)

    # Check if the column already exists
    if 'fecha_inicio_proceso' not in [c.name for c in reclamos.columns]:
        # Add the new column using raw SQL
        with engine.connect() as conn:
            conn.execute(text('ALTER TABLE TablaReclamos ADD COLUMN fecha_inicio_proceso DATETIME'))

    print("Columna 'fecha_inicio_proceso' añadida exitosamente.")
