"""
Pipeline de ingesta de datos WRC.

Uso:
    python -m ingestion.pipeline                  # descarga temporada activa
    python -m ingestion.pipeline --event-id 123   # descarga un evento concreto
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd

from ingestion import wrc_client as client
from ingestion import transformers as tr

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ingestion.pipeline")

# ── Paths ─────────────────────────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = _PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = _PROJECT_ROOT / "data" / "processed"


def _save_json(data: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("JSON guardado → %s", path.name)


def _save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info("CSV guardado → %s (%d filas)", path.name, len(df))


# ── Pasos del pipeline ────────────────────────────────────────────────────────

def step_season() -> list[dict]:
    """Paso 1: descarga y guarda los eventos de la temporada activa."""
    logger.info("── Paso 1: temporada activa ──")
    events = client.get_active_season()
    _save_json(events, RAW_DIR / "season_events.json")
    df = tr.transform_events(events)
    _save_csv(df, PROCESSED_DIR / "events.csv")
    return events


def step_event(event_id: int, event_name: str) -> None:
    """Paso 2: descarga y procesa un evento completo."""
    logger.info("── Paso 2: evento %d (%s) ──", event_id, event_name)
    safe_name = event_name.lower().replace(" ", "_")[:30]

    # — Itinerario + etapas —
    logger.info("  Descargando itinerario...")
    itinerary = client.get_itinerary(event_id)
    _save_json(itinerary, RAW_DIR / f"{safe_name}_itinerary.json")
    stages_df = tr.transform_stages(itinerary)
    _save_csv(stages_df, PROCESSED_DIR / f"{safe_name}_stages.csv")

    if stages_df.empty:
        logger.warning("  No se encontraron etapas para este evento.")
        return

    # — Entradas (pilotos) —
    logger.info("  Descargando pilotos...")
    try:
        entries = client.get_entries(event_id)
        _save_json(entries, RAW_DIR / f"{safe_name}_entries.json")
        entries_df = tr.transform_entries(entries)
        _save_csv(entries_df, PROCESSED_DIR / f"{safe_name}_entries.csv")
    except Exception as e:
        logger.warning("  No se pudieron descargar pilotos: %s", e)
        entries_df = pd.DataFrame()

    # — Tiempos de cada etapa —
    all_stage_times: list[pd.DataFrame] = []
    all_overall: list[pd.DataFrame] = []

    stage_ids = stages_df["stage_id"].tolist()
    logger.info("  Descargando tiempos de %d etapas...", len(stage_ids))

    for stage_id in stage_ids:
        stage_code = stages_df.loc[
            stages_df["stage_id"] == stage_id, "stage_code"
        ].values[0]
        logger.info("    Etapa %s (id=%d)...", stage_code, stage_id)

        try:
            raw_times = client.get_stage_times(event_id, stage_id)
            if raw_times:
                df_times = tr.transform_stage_times(raw_times, stage_id, event_id)
                df_times["stage_code"] = stage_code
                all_stage_times.append(df_times)
        except Exception as e:
            logger.warning("    stage_times %d fallido: %s", stage_id, e)

        try:
            raw_overall = client.get_overall_results(event_id, stage_id)
            if raw_overall:
                df_overall = tr.transform_overall_results(raw_overall, stage_id, event_id)
                df_overall["stage_code"] = stage_code
                all_overall.append(df_overall)
        except Exception as e:
            logger.warning("    overall %d fallido: %s", stage_id, e)

    # — Guardar consolidados —
    if all_stage_times:
        stage_times_df = pd.concat(all_stage_times, ignore_index=True)
        _save_csv(stage_times_df, PROCESSED_DIR / f"{safe_name}_stage_times.csv")

    if all_overall:
        overall_df = pd.concat(all_overall, ignore_index=True)
        _save_csv(overall_df, PROCESSED_DIR / f"{safe_name}_overall.csv")

    logger.info("  Evento %s completado.", event_name)


def run(event_id: int | None = None) -> None:
    """Punto de entrada principal del pipeline."""
    logger.info("═══ Rally Performance Analyzer — Pipeline de ingesta ═══")

    events = step_season()

    if not events:
        logger.error("No se encontraron eventos en la temporada activa.")
        sys.exit(1)

    # Si se especifica un evento concreto, solo descargamos ese
    if event_id is not None:
        match = [e for e in events if e.get("id") == event_id]
        if not match:
            logger.error("Evento %d no encontrado en la temporada activa.", event_id)
            sys.exit(1)
        targets = match
    else:
        # Por defecto: solo el primer evento completado (status=Completed)
        completed = [e for e in events if e.get("status") == "Completed"]
        targets = completed[:1] if completed else events[:1]

    for event in targets:
        eid = event.get("id")
        ename = event.get("name", f"event_{eid}")
        step_event(eid, ename)

    logger.info("═══ Pipeline finalizado ═══")


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WRC data ingestion pipeline")
    parser.add_argument(
        "--event-id",
        type=int,
        default=None,
        help="ID del evento a descargar (por defecto: primer evento completado)",
    )
    args = parser.parse_args()
    run(event_id=args.event_id)
