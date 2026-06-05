from __future__ import annotations
import logging
import os
import requests

logger = logging.getLogger(__name__)


def _get_api_base() -> str:
    """Obtiene la URL base de la API segun el entorno."""
    try:
        from pathlib import Path
        import streamlit as st
        # Streamlit emite "No secrets files found" al acceder a st.secrets aunque
        # el archivo no exista. Comprobamos las mismas rutas que usa internamente
        # y solo leemos secrets si el archivo existe, evitando el warning.
        _secrets_paths = (
            Path.home() / ".streamlit" / "secrets.toml",
            Path(".streamlit") / "secrets.toml",
        )
        if any(p.exists() for p in _secrets_paths):
            url = st.secrets.get("DASHBOARD_API_URL", None)
            if url:
                return url
    except Exception:
        pass
    return os.getenv("DASHBOARD_API_URL", "http://localhost:8000")


def _get(path: str, params: dict | None = None) -> dict | list | None:
    url = f"{_get_api_base()}{path}"
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        logger.error("No se puede conectar con la API en %s", _get_api_base())
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
