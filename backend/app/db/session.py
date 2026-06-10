"""
Conexion a rally.db y utilidades de sesion.

El fichero .db vive en la raiz del proyecto.
Si no existe, data_loader cae en fallback CSV automaticamente.
"""

from __future__ import annotations

import logging
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.app.db.models import Base

logger = logging.getLogger(__name__)

_PROJECT_ROOT = Path(__file__).resolve().parents[4]
DB_PATH = _PROJECT_ROOT / "rally.db"
DB_URL  = f"sqlite:///{DB_PATH}"


def get_engine(db_url: str = DB_URL):
    return create_engine(db_url, connect_args={"check_same_thread": False})


def get_session_factory(db_url: str = DB_URL):
    engine = get_engine(db_url)
    return sessionmaker(bind=engine)


def db_exists() -> bool:
    """Comprueba si rally.db existe y tiene datos."""
    if not DB_PATH.exists():
        return False
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM events"))
            return result.scalar() > 0
    except Exception:
        return False


def init_db(db_url: str = DB_URL) -> None:
    """Crea todas las tablas si no existen."""
    engine = get_engine(db_url)
    Base.metadata.create_all(engine)
    logger.info("DB inicializada: %s", db_url)
