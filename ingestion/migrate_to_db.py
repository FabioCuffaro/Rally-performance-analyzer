"""
Migracion CSV → SQLite (Bloque 11).

Lee todos los CSVs de data/processed/ y los carga en rally.db.
Idempotente: borra y recrea las tablas en cada ejecucion.

Uso:
    python -m ingestion.migrate_to_db
    python -m ingestion.migrate_to_db --db-path /ruta/custom/rally.db
    python -m ingestion.migrate_to_db --dry-run   # solo valida, no escribe
"""

from __future__ import annotations

import argparse
import logging
import sqlite3
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from backend.app.db.models import Base

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_PROCESSED_DIR = _PROJECT_ROOT / "data" / "processed"

# Mapeo slug (underscore) → event_id
# Se usa para inyectar event_id en tablas que no lo tienen en el CSV
SLUG_TO_EVENT_ID: dict[str, int] = {
    "rallye_automobile_monte_carlo":      1,
    "rallye_automobile_monte_carlo_2025": 89918,
    "rally_sweden_2025":                  90090,
}

TABLE_PATTERNS = {
    "events":          ["events.csv"],
    "stages":          ["*_stages.csv"],
    "entries":         ["*_entries.csv"],
    "stage_times":     ["*_stage_times.csv"],
    "overall_results": ["*_overall.csv"],
}

REQUIRED_COLS = {
    "events":          ["event_id", "name"],
    "stages":          ["stage_id", "stage_code"],
    "entries":         ["entry_id", "driver_name"],
    "stage_times":     ["entry_id", "stage_id", "time_s"],
    "overall_results": ["entry_id", "position"],
}

ENSURE_COLS = {
    "entries":         ["car_model"],
    "overall_results": ["retirement_stage"],
}

# Tablas donde event_id NO esta en el CSV y debe inyectarse desde el slug
INJECT_EVENT_ID_TABLES = {"entries", "stages"}

# Sufijos de fichero que identifican la tabla (para extraer el slug)
TABLE_SUFFIXES = {
    "entries":         "_entries",
    "stages":          "_stages",
    "stage_times":     "_stage_times",
    "overall_results": "_overall",
}


def _glob_csvs(pattern: str) -> list[Path]:
    return sorted(_PROCESSED_DIR.glob(pattern))


def _extract_slug(path: Path, suffix: str) -> str:
    """Extrae el slug del nombre de fichero quitando el sufijo y la extension."""
    return path.stem.replace(suffix, "")


def _load_table(table_name: str, patterns: list[str]) -> pd.DataFrame:
    frames = []
    suffix = TABLE_SUFFIXES.get(table_name, "")

    for pattern in patterns:
        for path in _glob_csvs(pattern):
            if path.stat().st_size == 0:
                continue
            try:
                df = pd.read_csv(path, encoding="utf-8-sig")

                # Inyectar event_id si la tabla lo necesita y no lo tiene
                if table_name in INJECT_EVENT_ID_TABLES and "event_id" not in df.columns:
                    slug = _extract_slug(path, suffix)
                    event_id = SLUG_TO_EVENT_ID.get(slug)
                    if event_id is not None:
                        df.insert(0, "event_id", event_id)
                    else:
                        logger.warning("  No se encontro event_id para slug '%s'", slug)

                frames.append(df)
                logger.info("  Leido: %s (%d filas)", path.name, len(df))
            except Exception as e:
                logger.warning("  Error leyendo %s: %s", path.name, e)

    if not frames:
        logger.warning("  Sin datos para tabla '%s'", table_name)
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)

    for col in REQUIRED_COLS.get(table_name, []):
        if col not in df.columns:
            logger.warning("  Columna obligatoria '%s' no encontrada en '%s'", col, table_name)

    for col in ENSURE_COLS.get(table_name, []):
        if col not in df.columns:
            df[col] = None

    return df


def migrate(db_path: str | None = None, dry_run: bool = False) -> dict[str, int]:
    """Ejecuta la migracion completa CSV → SQLite."""
    from backend.app.db.session import DB_PATH as DEFAULT_DB_PATH

    db_file = Path(db_path) if db_path else DEFAULT_DB_PATH
    db_url  = f"sqlite:///{db_file}"

    logger.info("=== Migracion CSV → SQLite ===")
    logger.info("Destino: %s", db_file)
    logger.info("Fuente:  %s", _PROCESSED_DIR)

    if dry_run:
        logger.info("[DRY RUN] Solo validacion, no se escribe nada")

    # SQLAlchemy crea el schema; sqlite3 carga los datos (compatibilidad pandas)
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

    if not dry_run:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        logger.info("Schema creado en %s", db_file.name)

    stats: dict[str, int] = {}

    for table_name, patterns in TABLE_PATTERNS.items():
        logger.info("--- Tabla: %s ---", table_name)
        df = _load_table(table_name, patterns)

        if df.empty:
            stats[table_name] = 0
            continue

        # Deduplicar
        before = len(df)
        dedup_cols = {
            "entries":         ["entry_id", "event_id"],
            "stages":          ["stage_id"],
            "stage_times":     ["entry_id", "stage_id"],
            "overall_results": ["entry_id", "stage_id"],
            "events":          ["event_id"],
        }
        cols = dedup_cols.get(table_name, [])
        valid_cols = [c for c in cols if c in df.columns]
        if valid_cols:
            df = df.drop_duplicates(subset=valid_cols)
        after = len(df)
        if before != after:
            logger.info("  Deduplicados: %d → %d filas", before, after)

        if not dry_run:
            # Usar sqlite3 directamente para evitar incompatibilidades con pandas
            with sqlite3.connect(str(db_file)) as conn:
                df.to_sql(table_name, conn, if_exists="append", index=False)
            logger.info("  Insertadas: %d filas", after)
        else:
            logger.info("  [DRY RUN] Se insertarian: %d filas", after)

        stats[table_name] = after

    logger.info("=== Migracion completada ===")
    for t, n in stats.items():
        logger.info("  %-20s %d filas", t, n)

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Migracion CSV → SQLite")
    parser.add_argument("--db-path", type=str, default=None,
                        help="Ruta al fichero .db (default: rally.db en raiz)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validar sin escribir")
    args = parser.parse_args()

    stats = migrate(db_path=args.db_path, dry_run=args.dry_run)

    if all(v == 0 for v in stats.values()):
        logger.error("No se migraron datos. Revisa que data/processed/ tiene CSVs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
