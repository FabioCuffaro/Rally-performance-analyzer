"""
Tests del Bloque 1 — Ingesta de datos.

Validan los transformadores con datos de ejemplo (sin llamar a la API real).
"""

import pandas as pd
import pytest

from ingestion.transformers import (
    transform_entries,
    transform_events,
    transform_overall_results,
    transform_stage_times,
    transform_stages,
    _ms_to_seconds,
    _ms_to_timestr,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def test_ms_to_seconds_basic():
    assert _ms_to_seconds(90000) == 90.0

def test_ms_to_seconds_precision():
    assert _ms_to_seconds(90500) == 90.5

def test_ms_to_seconds_none():
    assert _ms_to_seconds(None) is None

def test_ms_to_timestr_basic():
    # 1 minuto 30 segundos = 90000 ms
    assert _ms_to_timestr(90000) == "00:01:30.000"

def test_ms_to_timestr_none():
    assert _ms_to_timestr(None) is None


# ── Eventos ───────────────────────────────────────────────────────────────────

MOCK_EVENTS = [
    {
        "id": 1,
        "name": "Rally Monte Carlo",
        "status": "Completed",
        "rally": {
            "country": {"name": "France", "iso2": "FR"}
        },
        "eventDays": [
            {"startDate": "2024-01-25"},
            {"finishDate": "2024-01-28"},
        ],
    }
]

def test_transform_events_columns():
    df = transform_events(MOCK_EVENTS)
    assert "event_id" in df.columns
    assert "name" in df.columns
    assert "country" in df.columns

def test_transform_events_values():
    df = transform_events(MOCK_EVENTS)
    assert df.iloc[0]["event_id"] == 1
    assert df.iloc[0]["name"] == "Rally Monte Carlo"
    assert df.iloc[0]["country"] == "France"

def test_transform_events_empty():
    df = transform_events([])
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


# ── Etapas ────────────────────────────────────────────────────────────────────

MOCK_ITINERARY = {
    "itineraryLegs": [
        {
            "name": "Leg 1",
            "itinerarySections": [
                {
                    "stages": [
                        {
                            "stageId": 101,
                            "code": "SS1",
                            "name": "Col de Turini",
                            "distance": 18.5,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                        {
                            "stageId": 102,
                            "code": "SS2",
                            "name": "La Cabanette",
                            "distance": 12.3,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                    ]
                }
            ],
        }
    ]
}

def test_transform_stages_count():
    df = transform_stages(MOCK_ITINERARY)
    assert len(df) == 2

def test_transform_stages_columns():
    df = transform_stages(MOCK_ITINERARY)
    assert "stage_id" in df.columns
    assert "stage_code" in df.columns
    assert "distance_km" in df.columns

def test_transform_stages_values():
    df = transform_stages(MOCK_ITINERARY)
    assert df.iloc[0]["stage_code"] == "SS1"
    assert df.iloc[0]["distance_km"] == 18.5


# ── Pilotos ───────────────────────────────────────────────────────────────────

MOCK_ENTRIES = [
    {
        "entryId": 201,
        "identifier": "1",
        "driver": {
            "fullName": "Sébastien Ogier",
            "code": "OGI",
            "country": {"iso2": "FR"},
        },
        "codriver": {"fullName": "Vincent Landais"},
        "manufacturer": {"name": "Toyota"},
        "group": {"name": "WRC"},
    }
]

def test_transform_entries_columns():
    df = transform_entries(MOCK_ENTRIES)
    assert "entry_id" in df.columns
    assert "driver_name" in df.columns
    assert "manufacturer" in df.columns

def test_transform_entries_values():
    df = transform_entries(MOCK_ENTRIES)
    assert df.iloc[0]["driver_name"] == "Sébastien Ogier"
    assert df.iloc[0]["manufacturer"] == "Toyota"
    assert df.iloc[0]["car_number"] == "1"


# ── Tiempos de etapa ──────────────────────────────────────────────────────────

MOCK_STAGE_TIMES = [
    {
        "entryId": 201,
        "position": 1,
        "elapsedDurationMs": 834500,
        "diffFirstMs": 0,
        "diffPrevMs": 0,
        "status": "Completed",
    },
    {
        "entryId": 202,
        "position": 2,
        "elapsedDurationMs": 835500,
        "diffFirstMs": 1000,
        "diffPrevMs": 1000,
        "status": "Completed",
    },
]

def test_transform_stage_times_count():
    df = transform_stage_times(MOCK_STAGE_TIMES, stage_id=101, event_id=1)
    assert len(df) == 2

def test_transform_stage_times_columns():
    df = transform_stage_times(MOCK_STAGE_TIMES, stage_id=101, event_id=1)
    assert "time_s" in df.columns
    assert "diff_first_s" in df.columns
    assert "time_str" in df.columns

def test_transform_stage_times_conversion():
    df = transform_stage_times(MOCK_STAGE_TIMES, stage_id=101, event_id=1)
    assert df.iloc[0]["time_s"] == 834.5
    assert df.iloc[1]["diff_first_s"] == 1.0

def test_transform_stage_times_sorted():
    """Los tiempos deben estar ordenados por posición."""
    df = transform_stage_times(MOCK_STAGE_TIMES, stage_id=101, event_id=1)
    assert df.iloc[0]["position"] == 1
    assert df.iloc[1]["position"] == 2


# ── Clasificación general ─────────────────────────────────────────────────────

MOCK_OVERALL = [
    {
        "entryId": 201,
        "position": 1,
        "totalTimeMs": 5000000,
        "diffFirstMs": 0,
        "penaltyTimeMs": 0,
    },
    {
        "entryId": 202,
        "position": 2,
        "totalTimeMs": 5015000,
        "diffFirstMs": 15000,
        "penaltyTimeMs": 0,
    },
]

def test_transform_overall_results_count():
    df = transform_overall_results(MOCK_OVERALL, stage_id=101, event_id=1)
    assert len(df) == 2

def test_transform_overall_results_leader_gap():
    df = transform_overall_results(MOCK_OVERALL, stage_id=101, event_id=1)
    assert df.iloc[0]["diff_first_s"] == 0.0
    assert df.iloc[1]["diff_first_s"] == 15.0
