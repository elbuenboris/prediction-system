from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///prediction-system-database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Funcion para obtener sesion de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Funcion para inicializar la base de datos
def init_db():
    # Importar los modelos
    from .models.order_model import Order

    # Crear todas las tablas definidas en los modelos
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


# Funcion para obtener sesion directa (sin generator)
def get_db_session():
    return SessionLocal()
