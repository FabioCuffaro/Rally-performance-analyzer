"""
Tests Bloque 11 — Capa SQLite.

Validan:
1. Migracion CSV → SQLite genera tablas correctas
2. data_loader en modo DB devuelve los mismos datos que en modo CSV
3. La API sigue respondiendo igual con DB activa
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from ingestion.migrate_to_db import migrate
from backend.app.services import data_loader


# ── Fixture: DB de test construida desde los CSVs existentes ─────────────────

@pytest.fixture(scope="module")
def test_db_path(tmp_path_factory):
    """Crea una rally.db temporal con los CSVs del proyecto."""
    db = tmp_path_factory.mktemp("db") / "test_rally.db"
    stats = migrate(db_path=str(db))
    assert stats.get("events", 0) > 0, "Migracion no genero eventos"
    return db


# ── Tests de migracion ────────────────────────────────────────────────────────

def test_migration_creates_db(test_db_path):
    assert test_db_path.exists()
    assert test_db_path.stat().st_size > 0


def test_migration_events_table(test_db_path):
    with sqlite3.connect(test_db_path) as conn:
        df = pd.read_sql("SELECT * FROM events", conn)
    assert len(df) >= 3  # mock, MC 2025, Sweden 2025
    assert "event_id" in df.columns
    assert "name" in df.columns


def test_migration_stages_table(test_db_path):
    with sqlite3.connect(test_db_path) as conn:
        df = pd.read_sql("SELECT * FROM stages", conn)
    assert len(df) >= 5  # al menos las 5 etapas mock
    for col in ["stage_id", "event_id", "stage_code", "distance_km", "surface"]:
        assert col in df.columns


def test_migration_entries_table(test_db_path):
    with sqlite3.connect(test_db_path) as conn:
        df = pd.read_sql("SELECT * FROM entries", conn)
    assert len(df) >= 6  # al menos los 6 pilotos mock
    for col in ["entry_id", "event_id", "driver_name", "manufacturer"]:
        assert col in df.columns


def test_migration_stage_times_table(test_db_path):
    with sqlite3.connect(test_db_path) as conn:
        df = pd.read_sql("SELECT * FROM stage_times", conn)
    assert len(df) >= 30  # 6 pilotos x 5 etapas mock
    for col in ["entry_id", "stage_id", "time_s", "position"]:
        assert col in df.columns


def test_migration_overall_table(test_db_path):
    with sqlite3.connect(test_db_path) as conn:
        df = pd.read_sql("SELECT * FROM overall_results", conn)
    assert len(df) >= 6  # al menos la clasificacion final mock
    for col in ["entry_id", "event_id", "position"]:
        assert col in df.columns


def test_migration_no_duplicates(test_db_path):
    """Verificar que no hay stage_times duplicados (entry_id, stage_id)."""
    with sqlite3.connect(test_db_path) as conn:
        df = pd.read_sql("SELECT * FROM stage_times", conn)
    dupes = df.duplicated(subset=["entry_id", "stage_id"]).sum()
    assert dupes == 0, f"Encontrados {dupes} duplicados en stage_times"


def test_migration_dry_run_no_file(tmp_path):
    """dry_run no debe crear fichero."""
    db = tmp_path / "should_not_exist.db"
    migrate(db_path=str(db), dry_run=True)
    assert not db.exists()


# ── Tests de data_loader en modo DB ──────────────────────────────────────────

@pytest.fixture
def loader_with_db(test_db_path, monkeypatch):
    """Parchea data_loader para usar la DB de test."""
    monkeypatch.setattr(data_loader, "_DB_PATH", test_db_path)
    data_loader.clear_cache()
    yield
    data_loader.clear_cache()


def test_loader_db_get_events(loader_with_db):
    df = data_loader.get_events()
    assert not df.empty
    assert "event_id" in df.columns
    assert len(df) >= 3


def test_loader_db_get_stages_mock(loader_with_db):
    df = data_loader.get_stages(1)
    assert not df.empty
    assert len(df) == 5
    assert "stage_code" in df.columns


def test_loader_db_get_entries_mock(loader_with_db):
    df = data_loader.get_entries(1)
    assert not df.empty
    assert len(df) == 6
    assert "driver_name" in df.columns


def test_loader_db_get_stage_times_mock(loader_with_db):
    df = data_loader.get_stage_times(1)
    assert not df.empty
    assert len(df) == 30
    assert "time_s" in df.columns


def test_loader_db_get_overall_mock(loader_with_db):
    df = data_loader.get_overall(1)
    assert not df.empty
    assert "position" in df.columns


def test_loader_db_enriched_stage_times(loader_with_db):
    df = data_loader.get_stage_times_enriched(1)
    assert not df.empty
    assert "driver_name" in df.columns
    assert "manufacturer" in df.columns


def test_loader_db_enriched_overall(loader_with_db):
    df = data_loader.get_overall_enriched(1)
    assert not df.empty
    assert "driver_name" in df.columns


def test_loader_db_monte_carlo_2025(loader_with_db):
    """Monte Carlo 2025 debe tener 62 pilotos en DB."""
    df = data_loader.get_entries(89918)
    assert not df.empty
    assert len(df) == 62


def test_loader_db_sweden_2025(loader_with_db):
    """Sweden 2025 debe tener 57 pilotos en DB."""
    df = data_loader.get_entries(90090)
    assert not df.empty
    assert len(df) == 57


def test_loader_db_stages_count_sweden(loader_with_db):
    """Sweden 2025 debe tener 18 etapas."""
    df = data_loader.get_stages(90090)
    assert not df.empty
    assert len(df) == 18


# ── Tests de fallback CSV (sin DB) ────────────────────────────────────────────

@pytest.fixture
def loader_without_db(monkeypatch, tmp_path):
    """Parchea data_loader para que no encuentre DB."""
    monkeypatch.setattr(data_loader, "_DB_PATH", tmp_path / "nonexistent.db")
    data_loader.clear_cache()
    yield
    data_loader.clear_cache()


def test_loader_csv_fallback_events(loader_without_db):
    df = data_loader.get_events()
    assert not df.empty
    assert "event_id" in df.columns


def test_loader_csv_fallback_stages(loader_without_db):
    df = data_loader.get_stages(1)
    assert not df.empty
    assert len(df) == 5


def test_loader_csv_fallback_entries(loader_without_db):
    df = data_loader.get_entries(1)
    assert not df.empty
    assert len(df) == 6


def test_loader_csv_fallback_stage_times(loader_without_db):
    df = data_loader.get_stage_times(1)
    assert not df.empty
    assert len(df) == 30
