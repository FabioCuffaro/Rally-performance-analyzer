"""
Cliente de la API para el dashboard.

Encapsula todas las llamadas al backend FastAPI.
"""

from __future__ import annotations

import logging
import os

import requests

logger = logging.getLogger(__name__)

_API_BASE = os.getenv("DASHBOARD_API_URL", "http://localhost:8000")


def _get(path: str, params: dict | None = None) -> dict | list | None:
    url = f"{_API_BASE}{path}"
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        logger.error("No se puede conectar con la API en %s", _API_BASE)
        return None
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error %s en %s", e.response.status_code, url)
        return None


def get_rallies() -> list[dict]:
    return _get("/rallies/") or []


def get_rally(event_id: int) -> dict | None:
    return _get(f"/rallies/{event_id}")


def get_stages() -> list[dict]:
    return _get("/stages/") or []


def get_stage_times(stage_id: int) -> dict | None:
    return _get(f"/stages/{stage_id}/times")


def get_drivers() -> list[dict]:
    return _get("/drivers/") or []


def get_classification() -> dict | None:
    return _get("/drivers/classification")


def get_evolution() -> list[dict]:
    return _get("/drivers/evolution") or []


def compare_drivers(entry_a: int, entry_b: int) -> dict | None:
    return _get("/drivers/compare", params={"entry_a": entry_a, "entry_b": entry_b})
