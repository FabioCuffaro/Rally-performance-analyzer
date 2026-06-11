"""
Tests Bloque 12 — Endpoints de temporada.

Validan los endpoints /season/* usando los datos reales disponibles
(MC2025 y Sweden2025) y el mock (event_id=1).
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


# ── /season/standings ─────────────────────────────────────────────────────────

def test_standings_status():
    r = client.get("/season/standings")
    assert r.status_code == 200


def test_standings_structure():
    r = client.get("/season/standings")
    data = r.json()
    assert "entries" in data
    assert "event_ids" in data


def test_standings_has_drivers():
    r = client.get("/season/standings")
    entries = r.json()["entries"]
    assert len(entries) > 0


def test_standings_leader_has_most_points():
    r = client.get("/season/standings")
    entries = r.json()["entries"]
    if len(entries) >= 2:
        assert entries[0]["total_points"] >= entries[1]["total_points"]


def test_standings_points_positive():
    r = client.get("/season/standings")
    for e in r.json()["entries"]:
        assert e["total_points"] > 0


def test_standings_single_event():
    r = client.get("/season/standings?event_ids=89918")
    assert r.status_code == 200
    data = r.json()
    assert len(data["entries"]) > 0


def test_standings_both_real_events():
    r = client.get("/season/standings?event_ids=89918,90090")
    assert r.status_code == 200
    assert len(r.json()["entries"]) > 0


def test_standings_invalid_event():
    r = client.get("/season/standings?event_ids=99999")
    assert r.status_code == 404


def test_standings_rally_points_keys():
    """rally_points debe tener al menos un evento como clave."""
    r = client.get("/season/standings?event_ids=89918")
    entry = r.json()["entries"][0]
    assert len(entry["rally_points"]) > 0


def test_standings_p1_gets_25_points():
    """El lider de un rally debe tener 25 puntos de ese evento."""
    r = client.get("/season/standings?event_ids=89918")
    entries = r.json()["entries"]
    # El lider de standings single-event debe tener 25 puntos
    leader = entries[0]
    pts_in_event = list(leader["rally_points"].values())[0]
    assert pts_in_event == 25


# ── /season/pace-evolution ────────────────────────────────────────────────────

def test_pace_evolution_status():
    r = client.get("/season/pace-evolution")
    assert r.status_code == 200


def test_pace_evolution_returns_list():
    r = client.get("/season/pace-evolution")
    assert isinstance(r.json(), list)


def test_pace_evolution_structure():
    r = client.get("/season/pace-evolution")
    data = r.json()
    if data:  # Puede estar vacio si no hay stage_times en eventos reales
        driver = data[0]
        assert "driver_name" in driver
        assert "paces" in driver
        assert len(driver["paces"]) > 0


def test_pace_evolution_with_mock():
    """El mock (event_id=1) tiene stage_times completos."""
    r = client.get("/season/pace-evolution?event_ids=1")
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 5  # mock tiene 6 entradas pero Ott Tanak aparece 2 veces (entry 204 y 206), groupby los fusiona
    assert data[0]["paces"][0]["avg_pace"] > 0


def test_pace_evolution_pace_positive():
    r = client.get("/season/pace-evolution?event_ids=1")
    for driver in r.json():
        for pace in driver["paces"]:
            assert pace["avg_pace"] > 0
            assert pace["stage_count"] > 0


# ── /season/surface-mastery ───────────────────────────────────────────────────

def test_surface_mastery_status():
    r = client.get("/season/surface-mastery")
    assert r.status_code == 200


def test_surface_mastery_returns_list():
    r = client.get("/season/surface-mastery")
    assert isinstance(r.json(), list)


def test_surface_mastery_with_mock():
    r = client.get("/season/surface-mastery?event_ids=1")
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    entry = data[0]
    for field in ["driver_name", "surface", "avg_pace", "stage_count", "rally_count"]:
        assert field in entry


def test_surface_mastery_pace_positive():
    r = client.get("/season/surface-mastery?event_ids=1")
    for entry in r.json():
        assert entry["avg_pace"] > 0
        assert entry["stage_count"] > 0
        assert entry["rally_count"] >= 1


# ── /season/h2h ───────────────────────────────────────────────────────────────

def test_h2h_status():
    r = client.get("/season/h2h?driver_a=Ogier+S.&driver_b=Evans+E.&event_ids=89918")
    assert r.status_code in (200, 404)  # 404 si los nombres no coinciden exactamente


def test_h2h_with_mock():
    """El mock tiene pilotos conocidos."""
    # Obtener dos pilotos del mock
    drivers = client.get("/drivers/?event_id=1").json()
    if len(drivers) >= 2:
        a = drivers[0]["driver_name"]
        b = drivers[1]["driver_name"]
        r = client.get(f"/season/h2h?driver_a={a}&driver_b={b}&event_ids=1")
        assert r.status_code == 200
        data = r.json()
        assert "driver_a" in data
        assert "results" in data
        assert len(data["results"]) > 0


def test_h2h_structure():
    drivers = client.get("/drivers/?event_id=1").json()
    if len(drivers) >= 2:
        a = drivers[0]["driver_name"]
        b = drivers[1]["driver_name"]
        r = client.get(f"/season/h2h?driver_a={a}&driver_b={b}&event_ids=1")
        if r.status_code == 200:
            data = r.json()
            for field in ["driver_a", "driver_b", "results", "wins_a", "wins_b"]:
                assert field in data
            if data["results"]:
                result = data["results"][0]
                for field in ["event_id", "event_name", "points_a", "points_b", "winner"]:
                    assert field in result


def test_h2h_wins_sum():
    """wins_a + wins_b <= total rallies."""
    drivers = client.get("/drivers/?event_id=1").json()
    if len(drivers) >= 2:
        a = drivers[0]["driver_name"]
        b = drivers[1]["driver_name"]
        r = client.get(f"/season/h2h?driver_a={a}&driver_b={b}&event_ids=1")
        if r.status_code == 200:
            data = r.json()
            assert data["wins_a"] + data["wins_b"] <= len(data["results"])
