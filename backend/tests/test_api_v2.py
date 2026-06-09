"""
Tests Bloque 7 — Nuevos endpoints V2.

Usa los datos mock (event_id=1) que tienen stage_times completos
para que pace, consistency y stage-wins funcionen en los tests.
Los tests existentes en test_api.py siguen sin cambios.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.data_loader import clear_cache

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_cache():
    clear_cache()
    yield
    clear_cache()


# ── /drivers/?event_id= ───────────────────────────────────────────────────────

def test_list_drivers_default_event():
    """Sin event_id usa el mock (6 pilotos)."""
    r = client.get("/drivers/")
    assert r.status_code == 200
    assert len(r.json()) == 6

def test_list_drivers_event_89918():
    """Monte Carlo 2025 real tiene 62 pilotos."""
    r = client.get("/drivers/?event_id=89918")
    assert r.status_code == 200
    assert len(r.json()) == 62

def test_list_drivers_event_90090():
    """Sweden 2025 real tiene 57 pilotos."""
    r = client.get("/drivers/?event_id=90090")
    assert r.status_code == 200
    assert len(r.json()) == 57


# ── /drivers/classification?event_id= ────────────────────────────────────────

def test_classification_real_event():
    """Monte Carlo 2025 real — clasificacion con 62 pilotos."""
    r = client.get("/drivers/classification?event_id=89918")
    assert r.status_code == 200
    data = r.json()
    assert "entries" in data
    assert len(data["entries"]) == 62

def test_classification_leader_real():
    """Lider de Monte Carlo 2025 debe ser Ogier."""
    r = client.get("/drivers/classification?event_id=89918")
    leader = r.json()["entries"][0]
    assert leader["position"] == 1
    assert "Ogier" in leader["driver_name"]

def test_classification_leader_gap_zero_real():
    r = client.get("/drivers/classification?event_id=89918")
    leader = r.json()["entries"][0]
    assert leader["diff_first_s"] == 0.0


# ── /drivers/{entry_id}/pace ──────────────────────────────────────────────────

def test_driver_pace_status():
    """Pace del piloto 201 (mock) — debe devolver 200."""
    r = client.get("/drivers/201/pace")
    assert r.status_code == 200

def test_driver_pace_has_stages():
    r = client.get("/drivers/201/pace")
    data = r.json()
    assert "stages" in data
    assert len(data["stages"]) > 0

def test_driver_pace_positive_values():
    r = client.get("/drivers/201/pace")
    for stage in r.json()["stages"]:
        assert stage["pace_s_per_km"] > 0
        assert stage["distance_km"] > 0

def test_driver_pace_has_avg():
    r = client.get("/drivers/201/pace")
    data = r.json()
    assert "avg_pace" in data
    assert data["avg_pace"] > 0

def test_driver_pace_not_found():
    r = client.get("/drivers/9999/pace")
    assert r.status_code == 404

def test_driver_pace_no_stage_times_event():
    """Monte Carlo 2025 no tiene stage_times — debe devolver 404."""
    r = client.get("/drivers/201/pace?event_id=89918")
    assert r.status_code == 404


# ── /drivers/{entry_id}/consistency ──────────────────────────────────────────

def test_driver_consistency_status():
    r = client.get("/drivers/201/consistency")
    assert r.status_code == 200

def test_driver_consistency_fields():
    r = client.get("/drivers/201/consistency")
    data = r.json()
    for field in ["entry_id", "driver_name", "pace_mean", "pace_std", "stage_count"]:
        assert field in data

def test_driver_consistency_pace_mean_positive():
    r = client.get("/drivers/201/consistency")
    assert r.json()["pace_mean"] > 0

def test_driver_consistency_stage_count():
    r = client.get("/drivers/201/consistency")
    assert r.json()["stage_count"] == 5  # mock tiene 5 etapas

def test_driver_consistency_not_found():
    r = client.get("/drivers/9999/consistency")
    assert r.status_code == 404


# ── /drivers/surface-stats ────────────────────────────────────────────────────

def test_surface_stats_status():
    r = client.get("/drivers/surface-stats")
    assert r.status_code == 200

def test_surface_stats_returns_list():
    r = client.get("/drivers/surface-stats")
    assert isinstance(r.json(), list)

def test_surface_stats_has_drivers():
    r = client.get("/drivers/surface-stats")
    assert len(r.json()) > 0

def test_surface_stats_structure():
    r = client.get("/drivers/surface-stats")
    driver = r.json()[0]
    assert "entry_id" in driver
    assert "stats" in driver
    assert len(driver["stats"]) > 0

def test_surface_stats_values_positive():
    r = client.get("/drivers/surface-stats")
    for driver in r.json():
        for stat in driver["stats"]:
            assert stat["avg_pace"] > 0
            assert stat["stage_count"] > 0


# ── /rallies/{event_id}/stage-wins ───────────────────────────────────────────

def test_stage_wins_status():
    r = client.get("/rallies/1/stage-wins")
    assert r.status_code == 200

def test_stage_wins_structure():
    r = client.get("/rallies/1/stage-wins")
    data = r.json()
    assert "event_id" in data
    assert "wins" in data
    assert data["event_id"] == 1

def test_stage_wins_total_equals_stages():
    """El total de stage wins debe ser igual al numero de etapas."""
    r = client.get("/rallies/1/stage-wins")
    wins = r.json()["wins"]
    total_wins = sum(w["win_count"] for w in wins)
    assert total_wins == 5  # mock tiene 5 etapas

def test_stage_wins_fields():
    r = client.get("/rallies/1/stage-wins")
    win = r.json()["wins"][0]
    for field in ["entry_id", "driver_name", "manufacturer", "win_count", "stage_codes"]:
        assert field in win

def test_stage_wins_sweden():
    """Sweden 2025 tiene stage_times (1 ganador por etapa = 18 wins total)."""
    r = client.get("/rallies/90090/stage-wins")
    assert r.status_code == 200
    wins = r.json()["wins"]
    total_wins = sum(w["win_count"] for w in wins)
    assert total_wins == 18  # 18 etapas

def test_stage_wins_event_not_found():
    r = client.get("/rallies/9999/stage-wins")
    assert r.status_code == 404


# ── /drivers/momentum ────────────────────────────────────────────────────────

def test_momentum_status():
    r = client.get("/drivers/momentum")
    assert r.status_code == 200

def test_momentum_returns_list():
    r = client.get("/drivers/momentum")
    assert isinstance(r.json(), list)

def test_momentum_has_drivers():
    r = client.get("/drivers/momentum")
    assert len(r.json()) > 0

def test_momentum_fields():
    r = client.get("/drivers/momentum")
    entry = r.json()[0]
    for field in ["entry_id", "driver_name", "momentum"]:
        assert field in entry
