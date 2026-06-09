"""
Tests del Bloque 6 -- Scraper eWRC.

Validan los parsers con fixtures HTML estaticas (sin llamadas de red).
Las fixtures reproducen la estructura HTML real de ewrc-results.com
segun la documentacion del codigo de referencia (ArkaitzUlibarri/ewrc-results).
"""

from __future__ import annotations

import pytest
from bs4 import BeautifulSoup

from ingestion.ewrc_scraper import (
    parse_itinerary,
    parse_final_results,
    parse_stage_times,
    _parse_km,
    _parse_time_text,
    _split_driver_codriver,
    _make_driver_code,
    _calculate_positions_and_gaps,
)
import pandas as pd


# ── Fixtures HTML ─────────────────────────────────────────────────────────────

ITINERARY_HTML = """
<html><body>
<div class="harm-main">
  <div class="text-muted">Leg 1 - Thursday</div>
  <div class="harm d-flex">
    <div class="harm-ss">SS1</div>
    <div class="harm-stage">Col de Turini</div>
    <div class="harm-km">18.55 km</div>
  </div>
  <div class="harm d-flex">
    <div class="harm-ss">SS2</div>
    <div class="harm-stage">La Cabanette - Col de Braus</div>
    <div class="harm-km">12.30 km</div>
  </div>
  <div class="harm d-flex harm-service">
    <div class="harm-ss"><i class="fas fa-tools"></i></div>
    <div class="harm-stage">Service Park Gap</div>
    <div class="harm-km"></div>
  </div>
  <div class="text-muted">Leg 2 - Friday</div>
  <div class="harm d-flex">
    <div class="harm-ss">SS3</div>
    <div class="harm-stage">Luceam - Lantosque</div>
    <div class="harm-km">22.10 km</div>
  </div>
</div>
</body></html>
"""

FINAL_RESULTS_HTML = """
<html><body>
<div class="final-results">
  <table class="results">
    <thead>
      <tr><th>Pos</th><th>No</th><th>Driver/Co-driver</th><th>Car</th><th>Group</th><th>Total</th><th>Gap</th></tr>
    </thead>
    <tbody>
      <tr>
        <td class="final-results-number">1.</td>
        <td>#17</td>
        <td class="final-entry"><a href="/entryinfo/89918/17">Ogier S. - Landais V.</a></td>
        <td class="font-weight-bold lh-130">Toyota GR Yaris Rally1<span>Toyota Gazoo Racing WRT</span></td>
        <td class="fs-091">WRC / RC1</td>
        <td class="font-weight-bold text-left">3:19:06.1</td>
        <td></td>
      </tr>
      <tr>
        <td class="final-results-number">2.</td>
        <td>#33</td>
        <td class="final-entry"><a href="/entryinfo/89918/33">Evans E. - Martin S.</a></td>
        <td class="font-weight-bold lh-130">Toyota GR Yaris Rally1<span>Toyota Gazoo Racing WRT</span></td>
        <td class="fs-091">WRC / RC1</td>
        <td class="font-weight-bold text-left">3:19:24.6</td>
        <td>+18.5</td>
      </tr>
      <tr>
        <td class="final-results-number">3.</td>
        <td>#16</td>
        <td class="final-entry"><a href="/entryinfo/89918/16">Fourmaux A. - Coria A.</a></td>
        <td class="font-weight-bold lh-130">Hyundai i20 N Rally1<span>Hyundai Shell Mobis WRT</span></td>
        <td class="fs-091">WRC / RC1</td>
        <td class="font-weight-bold text-left">3:19:32.1</td>
        <td>+26.0</td>
      </tr>
    </tbody>
  </table>
</div>
</body></html>
"""

STAGE_TIMES_HTML = """
<html><body>
<table class="results">
  <thead>
    <tr>
      <th>Driver</th>
      <th>SS1</th>
      <th>SS2</th>
      <th>SS3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Ogier S.</td>
      <td>13:54.5</td>
      <td>10:12.3</td>
      <td>18:30.1</td>
    </tr>
    <tr>
      <td>Evans E.</td>
      <td>13:56.2</td>
      <td>10:13.8</td>
      <td>18:31.4</td>
    </tr>
    <tr>
      <td>Fourmaux A.</td>
      <td>13:57.0</td>
      <td>10:15.1</td>
      <td>18:32.6</td>
    </tr>
  </tbody>
</table>
</body></html>
"""

EMPTY_HTML = "<html><body><p>No data</p></body></html>"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


# ── Tests: _parse_km ──────────────────────────────────────────────────────────

def test_parse_km_basic():
    assert _parse_km("18.55 km") == 18.55

def test_parse_km_no_unit():
    assert _parse_km("12.30") == 12.30

def test_parse_km_comma():
    assert _parse_km("22,10 km") == 22.10

def test_parse_km_empty():
    assert _parse_km("") == 0.0

def test_parse_km_invalid():
    assert _parse_km("n/a") == 0.0


# ── Tests: _parse_time_text ───────────────────────────────────────────────────

def test_parse_time_stage_format():
    # Formato MM:SS.t (tiempo por etapa)
    t, s = _parse_time_text("13:54.5")
    assert t == pytest.approx(834.5, abs=0.1)
    assert s == "13:54.5"

def test_parse_time_rally_format():
    # Formato H:MM:SS.t (tiempo total de rally)
    t, s = _parse_time_text("3:19:06.1")
    assert t == pytest.approx(11946.1, abs=0.1)
    assert s == "3:19:06.1"

def test_parse_time_dash():
    t, s = _parse_time_text("-")
    assert t is None
    assert s is None

def test_parse_time_dnf():
    t, s = _parse_time_text("DNF")
    assert t is None

def test_parse_time_empty():
    t, s = _parse_time_text("")
    assert t is None


# ── Tests: _split_driver_codriver ─────────────────────────────────────────────

def test_split_driver_dash():
    d, c = _split_driver_codriver("Ogier S. - Landais V.")
    assert d == "Ogier S."
    assert c == "Landais V."

def test_split_driver_slash():
    d, c = _split_driver_codriver("Evans E. / Martin S.")
    assert d == "Evans E."
    assert c == "Martin S."

def test_split_driver_no_separator():
    d, c = _split_driver_codriver("Ogier Sebastien")
    assert d == "Ogier Sebastien"
    assert c == ""


# ── Tests: _make_driver_code ──────────────────────────────────────────────────

def test_make_driver_code():
    assert _make_driver_code("Ogier S.") == "OGI"

def test_make_driver_code_short():
    assert _make_driver_code("Ev") == "EV"

def test_make_driver_code_empty():
    assert _make_driver_code("") == ""


# ── Tests: parse_itinerary ────────────────────────────────────────────────────

def test_parse_itinerary_count():
    soup = _soup(ITINERARY_HTML)
    df = parse_itinerary(soup, event_id=89918)
    assert len(df) == 3  # SS1, SS2, SS3 (service ignorado)

def test_parse_itinerary_columns():
    soup = _soup(ITINERARY_HTML)
    df = parse_itinerary(soup, event_id=89918)
    for col in ["stage_id", "stage_code", "name", "distance_km", "surface", "leg_name", "status"]:
        assert col in df.columns

def test_parse_itinerary_stage_codes():
    soup = _soup(ITINERARY_HTML)
    df = parse_itinerary(soup, event_id=89918)
    codes = df["stage_code"].tolist()
    assert "SS1" in codes
    assert "SS2" in codes
    assert "SS3" in codes

def test_parse_itinerary_distances():
    soup = _soup(ITINERARY_HTML)
    df = parse_itinerary(soup, event_id=89918)
    ss1 = df[df["stage_code"] == "SS1"].iloc[0]
    assert ss1["distance_km"] == pytest.approx(18.55)

def test_parse_itinerary_leg_changes():
    soup = _soup(ITINERARY_HTML)
    df = parse_itinerary(soup, event_id=89918)
    # SS1 y SS2 en Leg 1, SS3 en Leg 2
    assert df[df["stage_code"] == "SS1"].iloc[0]["leg_name"] == "Leg 1"
    assert df[df["stage_code"] == "SS3"].iloc[0]["leg_name"] == "Leg 2"

def test_parse_itinerary_empty():
    soup = _soup(EMPTY_HTML)
    df = parse_itinerary(soup, event_id=89918)
    assert df.empty


# ── Tests: parse_final_results ────────────────────────────────────────────────

def test_parse_final_results_entries_count():
    soup = _soup(FINAL_RESULTS_HTML)
    entries_df, _ = parse_final_results(soup, event_id=89918)
    assert len(entries_df) == 3

def test_parse_final_results_entries_columns():
    soup = _soup(FINAL_RESULTS_HTML)
    entries_df, _ = parse_final_results(soup, event_id=89918)
    for col in ["entry_id", "driver_name", "manufacturer", "car_number", "group"]:
        assert col in entries_df.columns

def test_parse_final_results_drivers():
    soup = _soup(FINAL_RESULTS_HTML)
    entries_df, _ = parse_final_results(soup, event_id=89918)
    drivers = entries_df["driver_name"].tolist()
    assert any("Ogier" in d for d in drivers)
    assert any("Evans" in d for d in drivers)

def test_parse_final_results_manufacturers():
    soup = _soup(FINAL_RESULTS_HTML)
    entries_df, _ = parse_final_results(soup, event_id=89918)
    manufacturers = entries_df["manufacturer"].tolist()
    assert "Toyota" in manufacturers
    assert "Hyundai" in manufacturers

def test_parse_final_results_overall_count():
    soup = _soup(FINAL_RESULTS_HTML)
    _, overall_df = parse_final_results(soup, event_id=89918)
    assert len(overall_df) == 3

def test_parse_final_results_overall_positions():
    soup = _soup(FINAL_RESULTS_HTML)
    _, overall_df = parse_final_results(soup, event_id=89918)
    positions = sorted(overall_df["position"].tolist())
    assert positions == [1, 2, 3]

def test_parse_final_results_leader_gap_zero():
    soup = _soup(FINAL_RESULTS_HTML)
    _, overall_df = parse_final_results(soup, event_id=89918)
    leader = overall_df[overall_df["position"] == 1].iloc[0]
    assert leader["diff_first_s"] == 0.0

def test_parse_final_results_total_time():
    soup = _soup(FINAL_RESULTS_HTML)
    _, overall_df = parse_final_results(soup, event_id=89918)
    leader = overall_df[overall_df["position"] == 1].iloc[0]
    # 3:19:06.1 = 11946.1 segundos
    assert leader["total_time_s"] == pytest.approx(11946.1, abs=0.2)

def test_parse_final_results_empty():
    soup = _soup(EMPTY_HTML)
    entries_df, overall_df = parse_final_results(soup, event_id=89918)
    assert entries_df.empty
    assert overall_df.empty


# ── Tests: parse_stage_times ──────────────────────────────────────────────────

STAGES_DF = pd.DataFrame([
    {"stage_id": 89918001, "stage_code": "SS1", "distance_km": 18.55},
    {"stage_id": 89918002, "stage_code": "SS2", "distance_km": 12.30},
    {"stage_id": 89918003, "stage_code": "SS3", "distance_km": 22.10},
])

def test_parse_stage_times_row_count():
    soup = _soup(STAGE_TIMES_HTML)
    df = parse_stage_times(soup, event_id=89918, stages_df=STAGES_DF)
    # 3 pilotos x 3 etapas = 9 filas
    assert len(df) == 9

def test_parse_stage_times_columns():
    soup = _soup(STAGE_TIMES_HTML)
    df = parse_stage_times(soup, event_id=89918, stages_df=STAGES_DF)
    for col in ["event_id", "stage_id", "entry_id", "position", "time_s", "time_str",
                "diff_first_s", "stage_code", "status"]:
        assert col in df.columns

def test_parse_stage_times_positions():
    soup = _soup(STAGE_TIMES_HTML)
    df = parse_stage_times(soup, event_id=89918, stages_df=STAGES_DF)
    # Ogier debe ser P1 en cada etapa
    ss1 = df[df["stage_code"] == "SS1"].sort_values("position")
    assert ss1.iloc[0]["position"] == 1
    assert ss1.iloc[0]["time_s"] == pytest.approx(834.5, abs=0.2)

def test_parse_stage_times_leader_gap_zero():
    soup = _soup(STAGE_TIMES_HTML)
    df = parse_stage_times(soup, event_id=89918, stages_df=STAGES_DF)
    for stage_code in ["SS1", "SS2", "SS3"]:
        leader = df[(df["stage_code"] == stage_code) & (df["position"] == 1)]
        assert leader.iloc[0]["diff_first_s"] == 0.0

def test_parse_stage_times_gaps_positive():
    soup = _soup(STAGE_TIMES_HTML)
    df = parse_stage_times(soup, event_id=89918, stages_df=STAGES_DF)
    non_leaders = df[df["position"] > 1]
    assert (non_leaders["diff_first_s"] > 0).all()

def test_parse_stage_times_empty():
    soup = _soup(EMPTY_HTML)
    df = parse_stage_times(soup, event_id=89918, stages_df=STAGES_DF)
    assert df.empty


# ── Tests: _calculate_positions_and_gaps ─────────────────────────────────────

def test_calculate_positions_simple():
    df = pd.DataFrame([
        {"event_id": 1, "stage_id": 1, "entry_id": 201, "time_s": 100.0,
         "time_ms": 100000, "time_str": "1:40.0", "stage_code": "SS1", "status": "Completed"},
        {"event_id": 1, "stage_id": 1, "entry_id": 202, "time_s": 102.5,
         "time_ms": 102500, "time_str": "1:42.5", "stage_code": "SS1", "status": "Completed"},
    ])
    result = _calculate_positions_and_gaps(df)
    assert result[result["entry_id"] == 201].iloc[0]["position"] == 1
    assert result[result["entry_id"] == 202].iloc[0]["position"] == 2
    assert result[result["entry_id"] == 201].iloc[0]["diff_first_s"] == 0.0
    assert result[result["entry_id"] == 202].iloc[0]["diff_first_s"] == pytest.approx(2.5)
