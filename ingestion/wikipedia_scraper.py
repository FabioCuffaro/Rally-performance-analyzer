"""
Wikipedia scraper para datos de WRC 2025.

Usa la Wikipedia REST API v1 (no scraping HTML directo) para obtener tablas
parseadas de los artículos de cada rally WRC 2025.

Artículos disponibles (confirmados):
  rally-sweden-2025         → 2025_Rally_Sweden
  rally-de-portugal-2025    → 2025_Rally_de_Portugal
  rally-finland-2025        → 2025_Rally_Finland
  rally-chile-2025          → 2025_Rally_Chile
  central-european-rally-2025 → 2025_Central_European_Rally
  rally-japan-2025          → 2025_Rally_Japan

Estructura de tablas Wikipedia por rally:
  tabla[0..3]: entradas por categoría (No., Driver, Co-Driver, Car, Eligibility, Tyre)
  tabla[4]:    itinerario (Date, No./Stage, Time span, Stage name, Distance)
  tabla[5]:    clasificación final (Position, No., Driver, Co-driver, Car, Time, Diff)
  tabla[6]:    ganadores de etapa (Stage, Winners, Car, Time)
  tabla[7..9]: championship standings (Driver, Co-driver, Manufacturer)
"""

from __future__ import annotations

import hashlib
import logging
import re
import time
from pathlib import Path
from typing import Optional

import httpx
import pandas as pd
from bs4 import BeautifulSoup

from ingestion.ewrc_scraper import (
    _parse_time_text,
    _make_driver_code,
    _manufacturer_from_car_model,
    _calculate_positions_and_gaps,
    RAW_DIR,
)

logger = logging.getLogger(__name__)

WIKI_REST_API = "https://en.wikipedia.org/api/rest_v1/page/html"
WIKI_HEADERS = {
    "User-Agent": "RallyPerformanceAnalyzer/1.0 (educational project; developers9627@gmail.com)",
    "Accept": "text/html",
}
REQUEST_DELAY_S = 1.0

# Mapa: ewrc slug → artículo Wikipedia
SLUG_TO_WIKI: dict[str, str] = {
    "rally-sweden-2025": "2025_Rally_Sweden",
    "rally-de-portugal-2025": "2025_Rally_de_Portugal",
    "rally-finland-2025": "2025_Rally_Finland",
    "rally-chile-2025": "2025_Rally_Chile",
    "central-european-rally-2025": "2025_Central_European_Rally",
    "rally-japan-2025": "2025_Rally_Japan",
}

# Event IDs para rallies Wikipedia (usamos IDs ficticios coherentes cuando no conocemos el real)
WIKI_EVENT_IDS: dict[str, int] = {
    "rally-sweden-2025": 90090,
    "rally-de-portugal-2025": 90120,
    "rally-finland-2025": 90130,
    "rally-chile-2025": 90140,
    "central-european-rally-2025": 90150,
    "rally-japan-2025": 90160,
}

WIKI_CACHE_DIR = RAW_DIR / "wikipedia"


class WikiClient:
    def __init__(self, use_cache: bool = True, delay: float = REQUEST_DELAY_S):
        self.use_cache = use_cache
        self.delay = delay
        self._last_req: float = 0.0
        WIKI_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, article: str) -> Path:
        h = hashlib.md5(article.encode()).hexdigest()[:10]
        return WIKI_CACHE_DIR / f"{h}_{article[:40]}.html"

    def fetch_article(self, article: str) -> Optional[BeautifulSoup]:
        cache = self._cache_path(article)
        if self.use_cache and cache.exists():
            logger.info("Wiki cache hit: %s", article)
            return BeautifulSoup(cache.read_text(encoding="utf-8"), "html.parser")

        elapsed = time.time() - self._last_req
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        url = f"{WIKI_REST_API}/{article}"
        logger.info("Fetching Wikipedia: %s", article)
        try:
            with httpx.Client(headers=WIKI_HEADERS, timeout=20, follow_redirects=True) as client:
                r = client.get(url)
                self._last_req = time.time()
                if r.status_code != 200:
                    logger.warning("Wikipedia HTTP %d para %s", r.status_code, article)
                    return None
                html = r.text
                if self.use_cache:
                    cache.write_text(html, encoding="utf-8")
                return BeautifulSoup(html, "html.parser")
        except httpx.RequestError as e:
            logger.error("Error red Wikipedia %s: %s", article, e)
            return None


def _wiki_tables(soup: BeautifulSoup) -> list:
    """Devuelve solo las wikitables ordenadas como aparecen en el artículo."""
    return [t for t in soup.find_all("table") if "wikitable" in " ".join(t.get("class", []))]


def _cell_text(cell) -> str:
    """Texto limpio de una celda, eliminando referencias [1], notas y símbolos."""
    text = cell.get_text(separator=" ", strip=True)
    text = re.sub(r"\[[\w\s]+\]", "", text)  # referencias [1], [note 1]
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_wiki_entries(soup: BeautifulSoup, event_id: int) -> pd.DataFrame:
    """
    Parsea las tablas de entradas del artículo Wikipedia.
    Combina WRC + WRC2 + otras categorías (primeras 4 wikitables).

    Columnas: entry_id, driver_name, driver_code, codriver_name,
              manufacturer, car_number, car_model, group
    """
    tables = _wiki_tables(soup)
    rows = []
    entry_counter = 1

    # Las primeras N tablas hasta que la cabecera no tenga 'Driver'
    for table in tables:
        all_th_texts = [_cell_text(th) for th in table.find_all("th")]
        if "Driver" not in all_th_texts and "No." not in all_th_texts:
            break
        if "Stage name" in all_th_texts or "Position" in all_th_texts:
            break

        for tr in table.find_all("tr"):
            cells = tr.find_all(["td", "th"])
            if not cells:
                continue

            texts = [_cell_text(c) for c in cells]
            if len(texts) < 4:
                continue

            # Saltar filas de cabecera: primera celda es texto no numérico conocido
            if not texts[0] or not re.match(r"^\d+$", texts[0]):
                continue

            car_num = texts[0]
            driver = texts[1]
            codriver = texts[2]
            entrant = texts[3]
            car_model = texts[4] if len(texts) > 4 else ""
            eligibility = texts[5] if len(texts) > 5 else ""

            group = _eligibility_to_group(eligibility, car_model)
            manufacturer = _manufacturer_from_car_model(car_model)

            rows.append({
                "entry_id": event_id * 100 + entry_counter,
                "driver_name": driver,
                "driver_code": _make_driver_code(driver),
                "driver_nationality": "",
                "codriver_name": codriver,
                "manufacturer": manufacturer,
                "car_number": car_num,
                "car_model": car_model,
                "group": group,
            })
            entry_counter += 1

    df = pd.DataFrame(rows)
    logger.info("Wiki entries: %d pilotos", len(df))
    return df


def parse_wiki_stages(soup: BeautifulSoup, event_id: int) -> pd.DataFrame:
    """
    Parsea la tabla de itinerario Wikipedia.

    Columnas esperadas: Date | No. | Time span | Stage name | Distance
    """
    tables = _wiki_tables(soup)
    rows = []
    stage_counter = 1

    itinerary_table = None
    for t in tables:
        headers = [_cell_text(th) for th in t.find_all("th")]
        if "Stage name" in headers or "Stage" in headers:
            itinerary_table = t
            break

    if not itinerary_table:
        logger.warning("parse_wiki_stages: no se encontró tabla de itinerario")
        return pd.DataFrame()

    current_leg = 1

    for tr in itinerary_table.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue

        texts = [_cell_text(c) for c in cells]
        if not texts:
            continue

        # Fila de cabecera real (Date, No., Stage name...)
        if texts[0] in ("Date", "No.", "Stage", "Stage name"):
            continue

        # Detectar primera celda para clasificar la fila
        first = texts[0]

        # Fila de fecha de jornada: "13 February", "14 February", etc.
        if re.match(r"^\d+\s+\w+", first):
            current_leg += 1
            # La primera etapa del día puede estar en la segunda celda
            second = texts[1] if len(texts) > 1 else ""
            if second.upper().startswith("SS"):
                texts = texts[1:]  # procesar la etapa de esta misma fila
                first = texts[0]
            else:
                continue

        stage_code = first
        if not stage_code.upper().startswith("SS"):
            continue

        # texts: [stage_code, time_span?, stage_name, distance]
        if len(texts) >= 3:
            stage_name = texts[-2] if len(texts) >= 3 else texts[1]
            dist_text = texts[-1]
        elif len(texts) == 2:
            stage_name = texts[1]
            dist_text = "0"
        else:
            continue

        # Extraer distancia
        dist_match = re.search(r"([\d.,]+)\s*km", dist_text)
        distance_km = float(dist_match.group(1).replace(",", ".")) if dist_match else 0.0

        rows.append({
            "stage_id": event_id * 1000 + stage_counter,
            "stage_code": stage_code,
            "name": stage_name,
            "distance_km": distance_km,
            "surface": "Gravel",  # WRC Sweden es grava
            "leg_name": f"Leg {current_leg - 1}",
            "status": "Completed",
        })
        stage_counter += 1

    df = pd.DataFrame(rows)
    logger.info("Wiki stages: %d etapas", len(df))
    return df


def parse_wiki_overall(
    soup: BeautifulSoup,
    event_id: int,
    entries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Parsea la tabla de clasificación final Wikipedia.

    Cabeceras: Position | No. | Driver | Co-driver | Entrant | Car | Time | Difference
    La segunda fila de cabecera tiene sub-cols de puntos: Event | Class | ...
    """
    tables = _wiki_tables(soup)
    results_table = None
    for t in tables:
        headers = [_cell_text(th) for th in t.find_all("th")]
        if "Position" in headers and "Time" in headers:
            results_table = t
            break

    if not results_table:
        logger.warning("parse_wiki_overall: no se encontró tabla de resultados")
        return pd.DataFrame()

    rows_out = []

    # Wikipedia usa <th> tanto en cabeceras como en celdas de datos.
    # Procesamos todas las filas y filtramos por presencia de tiempo en el contenido.
    for texts in (
        [_cell_text(c) for c in tr.find_all(["td", "th"])]
        for tr in results_table.find_all("tr")
    ):
        if len(texts) < 6:
            continue

        # Detectar índice de tiempo (formato H:MM:SS.t)
        time_idx = None
        for i, t in enumerate(texts):
            if re.match(r"^\d+:\d{2}:\d{2}", t):
                time_idx = i
                break
        if time_idx is None:
            continue

        # Posición = primer número antes del car number
        # El car number es un dígito(s) que aparece antes del driver
        # Intentamos extraer pos, car_num, driver, time, diff
        time_str = texts[time_idx]
        total_time_s, _ = _parse_time_text(time_str)
        if total_time_s is None:
            continue

        diff_text = texts[time_idx + 1] if time_idx + 1 < len(texts) else ""
        diff_match = re.search(r"[\+]?([\d:\.]+)", diff_text)
        if diff_match and diff_text.strip() not in ("0", "0.0", ""):
            diff_str = diff_match.group(1)
            diff_s, _ = _parse_time_text(diff_str) if ":" in diff_str else (float(diff_str), None)
        else:
            diff_s = 0.0

        # Extraer posición global (primeros campos numéricos)
        pos = None
        car_num = None
        driver = None
        for j, t in enumerate(texts[:time_idx]):
            if re.match(r"^\d+$", t):
                if pos is None:
                    pos = int(t)
                elif car_num is None and int(t) != pos:
                    car_num = t
            elif t and not re.match(r"^\d+$", t) and driver is None and j >= 1:
                driver = t

        if pos is None:
            continue

        # Buscar entry_id por car_number o driver
        entry_id = _find_entry_id(entries_df, car_num, driver, event_id, pos)

        rows_out.append({
            "event_id": event_id,
            "stage_id": event_id * 1000 + 999,
            "entry_id": entry_id,
            "position": pos,
            "total_time_ms": int(total_time_s * 1000),
            "total_time_s": total_time_s,
            "total_time_str": time_str,
            "diff_first_ms": int(diff_s * 1000) if diff_s is not None else None,
            "diff_first_s": diff_s,
            "status": "Completed",
            "stage_code": "FINAL",
        })

    df = pd.DataFrame(rows_out)
    logger.info("Wiki overall: %d entradas en clasificacion", len(df))
    return df


def parse_wiki_stage_times(
    soup: BeautifulSoup,
    event_id: int,
    stages_df: pd.DataFrame,
    entries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Parsea la tabla de ganadores de etapa Wikipedia.
    Solo contiene el ganador de cada etapa (no todos los pilotos).

    Cabeceras: Stage | Winners | Car | Time | Class leaders
    """
    tables = _wiki_tables(soup)
    winners_table = None
    for t in tables:
        headers = [_cell_text(th) for th in t.find_all("th")]
        if "Winners" in headers:
            winners_table = t
            break

    if not winners_table:
        logger.warning("parse_wiki_stage_times: no se encontró tabla de ganadores")
        return pd.DataFrame()

    stage_code_to_id: dict[str, int] = {}
    if not stages_df.empty and "stage_code" in stages_df.columns:
        stage_code_to_id = dict(zip(stages_df["stage_code"], stages_df["stage_id"]))

    rows_out = []

    for tr in winners_table.find_all("tr"):
        # Wikipedia usa <th> en todas las celdas de esta tabla
        cells = tr.find_all(["td", "th"])
        texts = [_cell_text(c) for c in cells]
        if len(texts) < 3:
            continue

        stage_code = texts[0]
        # Saltar cabecera "Stage" y shakedown SD
        if not stage_code.upper().startswith("SS"):
            continue

        winners_text = texts[1]  # "Evans / Martin" o "Evans E. / Martin S."
        # Tiempo está en índice 3 si hay 5+ cols (con Class leaders), si no en 2
        time_text = texts[3] if len(texts) >= 4 else texts[2]

        time_s, time_str = _parse_time_text(time_text)
        if time_s is None:
            continue

        driver_part = winners_text.split("/")[0].strip()
        entry_id = _find_entry_by_name(entries_df, driver_part, event_id)
        stage_id = stage_code_to_id.get(stage_code, event_id * 1000)

        rows_out.append({
            "event_id": event_id,
            "stage_id": stage_id,
            "entry_id": entry_id,
            "position": 1,
            "time_ms": int(time_s * 1000),
            "time_s": time_s,
            "time_str": time_str,
            "diff_first_ms": 0,
            "diff_first_s": 0.0,
            "diff_prev_ms": 0,
            "diff_prev_s": 0.0,
            "status": "Completed",
            "stage_code": stage_code,
        })

    df = pd.DataFrame(rows_out)
    logger.info("Wiki stage times: %d ganadores de etapa", len(df))
    return df


def scrape_wiki_event(
    slug: str,
    event_id: int,
    client: Optional[WikiClient] = None,
) -> dict[str, pd.DataFrame]:
    """
    Descarga y parsea un evento WRC 2025 desde Wikipedia.

    Devuelve dict con DataFrames: stages, entries, overall, stage_times
    Devuelve None si el artículo no existe para este slug.
    """
    article = SLUG_TO_WIKI.get(slug)
    if not article:
        logger.info("No hay artículo Wikipedia para slug: %s", slug)
        return {}

    if client is None:
        client = WikiClient()

    soup = client.fetch_article(article)
    if soup is None:
        return {}

    entries_df = parse_wiki_entries(soup, event_id)
    stages_df = parse_wiki_stages(soup, event_id)
    overall_df = parse_wiki_overall(soup, event_id, entries_df)
    stage_times_df = parse_wiki_stage_times(soup, event_id, stages_df, entries_df)

    return {
        "stages": stages_df,
        "entries": entries_df,
        "overall": overall_df,
        "stage_times": stage_times_df,
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _eligibility_to_group(eligibility: str, car_model: str) -> str:
    """Mapea Championship eligibility a grupo WRC."""
    e = eligibility.lower()
    if "rc1" in e or "rally1" in car_model.lower():
        return "WRC"
    if "rc2" in e or "rally2" in car_model.lower():
        return "WRC2"
    if "rc3" in e or "rally3" in car_model.lower():
        return "WRC3"
    if "rc4" in e or "rally4" in car_model.lower():
        return "WRC4"
    if "driver, co-driver, manufacturer" in e:
        return "WRC"
    return "WRC"


def _find_entry_id(
    entries_df: pd.DataFrame,
    car_num: Optional[str],
    driver: Optional[str],
    event_id: int,
    position: int,
) -> int:
    """Busca entry_id por car_number primero, luego por nombre de piloto."""
    if entries_df.empty:
        return event_id * 100 + position

    if car_num and "car_number" in entries_df.columns:
        match = entries_df[entries_df["car_number"] == str(car_num)]
        if not match.empty:
            return int(match.iloc[0]["entry_id"])

    if driver and "driver_name" in entries_df.columns:
        driver_low = driver.lower()
        for _, row in entries_df.iterrows():
            if driver_low in str(row["driver_name"]).lower():
                return int(row["entry_id"])

    return event_id * 100 + position


def _find_entry_by_name(entries_df: pd.DataFrame, name: str, event_id: int) -> int:
    """Busca entry_id por fragmento de nombre."""
    if entries_df.empty or not name:
        return event_id * 100 + 1
    name_low = name.lower().split()[0] if name.split() else name.lower()
    for _, row in entries_df.iterrows():
        if name_low in str(row["driver_name"]).lower():
            return int(row["entry_id"])
    return event_id * 100 + 1
