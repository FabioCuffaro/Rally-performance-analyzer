"""
Tests del Bloque 2 — Endpoints FastAPI.

Usa TestClient con datos reales de los CSVs generados en el Bloque 1.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.data_loader import clear_cache

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_cache():
    """Limpia la caché antes de cada test para evitar contaminación."""
    clear_cache()
    yield
    clear_cache()


# ── /health ───────────────────────────────────────────────────────────────────

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── /rallies ──────────────────────────────────────────────────────────────────

def test_list_rallies_status():
    r = client.get("/rallies/")
    assert r.status_code == 200

def test_list_rallies_returns_list():
    r = client.get("/rallies/")
    assert isinstance(r.json(), list)

def test_list_rallies_not_empty():
    r = client.get("/rallies/")
    assert len(r.json()) > 0

def test_get_rally_by_id():
    r = client.get("/rallies/1")
    assert r.status_code == 200
    data = r.json()
    assert data["event_id"] == 1
    assert "name" in data

def test_get_rally_not_found():
    r = client.get("/rallies/9999")
    assert r.status_code == 404

def test_rally_has_required_fields():
    r = client.get("/rallies/1")
    data = r.json()
    for field in ["event_id", "name", "status", "country"]:
        assert field in data


# ── /stages ───────────────────────────────────────────────────────────────────

def test_list_stages_status():
    r = client.get("/stages/")
    assert r.status_code == 200

def test_list_stages_count():
    r = client.get("/stages/")
    assert len(r.json()) == 5  # SS1-SS5

def test_stage_has_required_fields():
    r = client.get("/stages/")
    stage = r.json()[0]
    for field in ["stage_id", "stage_code", "name", "distance_km", "surface"]:
        assert field in stage

def test_get_stage_times_status():
    r = client.get("/stages/101/times")
    assert r.status_code == 200

def test_get_stage_times_has_entries():
    r = client.get("/stages/101/times")
    data = r.json()
    assert "entries" in data
    assert len(data["entries"]) == 6

def test_get_stage_times_first_position():
    r = client.get("/stages/101/times")
    entries = r.json()["entries"]
    positions = [e["position"] for e in entries]
    assert 1 in positions

def test_get_stage_times_has_driver_name():
    r = client.get("/stages/101/times")
    entry = r.json()["entries"][0]
    assert entry["driver_name"] != ""

def test_get_stage_times_not_found():
    r = client.get("/stages/9999/times")
    assert r.status_code == 404


# ── /drivers ──────────────────────────────────────────────────────────────────

def test_list_drivers_status():
    r = client.get("/drivers/")
    assert r.status_code == 200

def test_list_drivers_count():
    r = client.get("/drivers/")
    assert len(r.json()) == 6

def test_driver_has_required_fields():
    r = client.get("/drivers/")
    driver = r.json()[0]
    for field in ["entry_id", "driver_name", "manufacturer", "car_number"]:
        assert field in driver


# ── /drivers/classification ───────────────────────────────────────────────────

def test_classification_status():
    r = client.get("/drivers/classification")
    assert r.status_code == 200

def test_classification_has_entries():
    r = client.get("/drivers/classification")
    data = r.json()
    assert "entries" in data
    assert len(data["entries"]) == 6

def test_classification_leader_gap_zero():
    r = client.get("/drivers/classification")
    leader = r.json()["entries"][0]
    assert leader["position"] == 1
    assert leader["diff_first_s"] == 0.0

def test_classification_has_driver_info():
    r = client.get("/drivers/classification")
    leader = r.json()["entries"][0]
    assert leader["driver_name"] != ""
    assert leader["manufacturer"] != ""


# ── /drivers/evolution ────────────────────────────────────────────────────────

def test_evolution_status():
    r = client.get("/drivers/evolution")
    assert r.status_code == 200

def test_evolution_all_drivers():
    r = client.get("/drivers/evolution")
    assert len(r.json()) == 6

def test_evolution_has_positions():
    r = client.get("/drivers/evolution")
    driver = r.json()[0]
    assert "positions" in driver
    assert len(driver["positions"]) == 5  # 5 etapas


# ── /drivers/compare ──────────────────────────────────────────────────────────

def test_compare_status():
    r = client.get("/drivers/compare?entry_a=201&entry_b=202")
    assert r.status_code == 200

def test_compare_has_both_drivers():
    r = client.get("/drivers/compare?entry_a=201&entry_b=202")
    data = r.json()
    assert "driver_a" in data
    assert "driver_b" in data

def test_compare_has_stage_times():
    r = client.get("/drivers/compare?entry_a=201&entry_b=202")
    data = r.json()
    assert len(data["stage_times_a"]) == 5
    assert len(data["stage_times_b"]) == 5

def test_compare_driver_not_found():
    r = client.get("/drivers/compare?entry_a=201&entry_b=9999")
    assert r.status_code == 404
