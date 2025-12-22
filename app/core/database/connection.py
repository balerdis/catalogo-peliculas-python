from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import config
from contextlib import contextmanager
import logging
from .models import Base

logger = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_connection()

    def _initialize_connection(self):
        try:
            database_url = self._build_database_url()
            self.engine = create_engine(
                database_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                pool_timeout=30,
                echo=config.DEBUG

            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            logger.info("Conexión a base de datos inicializada correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar la conexión a la base de datos: {e}")
            raise

    def _build_database_url(self):
        # Base de datos
        db_user = config.DB_USER
        db_password = config.DB_PASSWORD
        db_host = config.DB_HOST
        db_port = config.DB_PORT
        db_name = config.DB_NAME
        return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    
    @contextmanager
    def get_session(self):
        if not self.SessionLocal:
            raise RuntimeError("Base de datos aun no inicializada.")
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            logger.error(f"Error en la sesión de base de datos: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self):
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Tablas Creadas/Verificadas correctamente")
        except Exception as e:
            logger.error(f"Error al crear tablas: {e}")
            raise

    def drop_tables(self):
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Tablas eliminadas correctamente")
        except Exception as e:
            logger.error(f"Error al eliminar tablas: {e}")
            raise

    def close_connection(self):
        if self.engine:
            self.engine.dispose()
            logger.info("Conexión a la base de datos cerrada correctamente")
        else:
            logger.warning("No hay conexión a la base de datos para cerrar")

# Creo una instancia global de conectividad a la base de datos
db_connection = DatabaseConnection()