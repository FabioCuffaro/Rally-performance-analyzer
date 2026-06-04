"""
Cliente HTTP para la WRC Live Timing API.

Soporta dos modos controlados por la variable de entorno WRC_USE_MOCK:
  - WRC_USE_MOCK=false (default)  → llamadas reales a api.wrc.com
  - WRC_USE_MOCK=true             → datos mock locales (desarrollo offline)
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from ingestion import mock_data as mock

logger = logging.getLogger(__name__)

# ── Configuración ─────────────────────────────────────────────────────────────
_SEASON_URL = "https://api.wrc.com/contel-page/83388/calendar/active-season/"
_RESULTS_BASE = "https://api.wrc.com/results-api"
_TIMEOUT = 15.0


def _use_mock() -> bool:
    """Devuelve True si WRC_USE_MOCK=true en el entorno o .env."""
    return os.getenv("WRC_USE_MOCK", "false").lower() == "true"


def _get(url: str, params: dict[str, Any] | None = None) -> Any:
    """Realiza una petición GET y devuelve el JSON parseado."""
    try:
        response = httpx.get(url, params=params, timeout=_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error %s al llamar %s", e.response.status_code, url)
        raise
    except httpx.RequestError as e:
        logger.error("Error de conexión al llamar %s: %s", url, e)
        raise


# ── Endpoints ─────────────────────────────────────────────────────────────────

def get_active_season() -> list[dict]:
    """Devuelve la lista de eventos de la temporada activa."""
    if _use_mock():
        logger.info("[MOCK] Cargando temporada activa desde mock_data")
        items = mock.MOCK_SEASON["rallyEvents"]["items"]
        logger.info("Temporada activa (mock): %d eventos", len(items))
        return items

    data = _get(_SEASON_URL)
    items = data.get("rallyEvents", {}).get("items", [])
    logger.info("Temporada activa: %d eventos encontrados", len(items))
    return items


def get_itinerary(event_id: int) -> dict:
    """Devuelve el itinerario completo de un evento."""
    if _use_mock():
        logger.info("[MOCK] Cargando itinerario para event_id=%d", event_id)
        return mock.MOCK_ITINERARY

    url = f"{_RESULTS_BASE}/rally-event/{event_id}/itinerary"
    return _get(url)


def get_entries(event_id: int) -> list[dict]:
    """Devuelve la lista de pilotos inscritos en un evento."""
    if _use_mock():
        logger.info("[MOCK] Cargando pilotos para event_id=%d", event_id)
        return mock.MOCK_ENTRIES

    url = f"{_RESULTS_BASE}/rally-event/{event_id}/cars"
    return _get(url)


def get_stage_times(event_id: int, stage_id: int) -> list[dict]:
    """Devuelve los tiempos de todos los pilotos en una etapa concreta."""
    if _use_mock():
        logger.info("[MOCK] Cargando stage_times para stage_id=%d", stage_id)
        return mock.MOCK_STAGE_TIMES.get(stage_id, [])

    url = (
        f"{_RESULTS_BASE}/rally-event/{event_id}"
        f"/stage-times/stage-external/{stage_id}"
    )
    return _get(url)


def get_overall_results(event_id: int, stage_id: int) -> list[dict]:
    """Devuelve la clasificación general acumulada hasta una etapa dada."""
    if _use_mock():
        logger.info("[MOCK] Cargando overall para stage_id=%d", stage_id)
        return mock.MOCK_OVERALL.get(stage_id, [])

    url = f"{_RESULTS_BASE}/rally-event/{event_id}/results/{stage_id}/stage-overall"
    return _get(url)


def get_split_times(event_id: int, stage_id: int) -> dict:
    """Devuelve los split times de una etapa."""
    if _use_mock():
        logger.info("[MOCK] Split times no disponibles en mock, devolviendo vacío")
        return {}

    url = (
        f"{_RESULTS_BASE}/rally-event/{event_id}"
        f"/stage-times/stage-external/{stage_id}/split-times"
    )
    return _get(url)
