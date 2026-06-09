"""
eWRC-results.com scraper -- Bloque 6.

Estrategia de datos (ewrc usa Next.js con SSR parcial):
  - /event/{id}-{slug}/final-results  → SSR completo (~1MB), contiene entries + overall
  - /event/{id}-{slug}/itinerary      → CSR vacío, sin datos
  - /times/{id}-{slug}/               → CSR vacío, sin datos

parse_final_results()   → fixtures de test con HTML estático (legacy)
parse_final_results_v2() → HTML Tailwind real de ewrc (nueva estructura)

Salida CSV (misma estructura que V1):
  {slug}_stages.csv
  {slug}_entries.csv
  {slug}_stage_times.csv
  {slug}_overall.csv
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

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────

BASE_URL = "https://ewrc-results.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Rate limiting etico: 1 request por segundo
REQUEST_DELAY_S = 1.0

# Rallies WRC 2025 soportados (event_id, slug)
WRC_2025_EVENTS = [
    (89918, "rallye-automobile-monte-carlo-2025"),
    (90090, "rally-sweden-2025"),
    (90091, "safari-rally-kenya-2025"),
]

# ── Paths ─────────────────────────────────────────────────────────────────────

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = _PROJECT_ROOT / "data" / "raw" / "ewrc"
PROCESSED_DIR = _PROJECT_ROOT / "data" / "processed"


# ── HTTP Client con cache ─────────────────────────────────────────────────────

class EwrcClient:
    """
    Cliente HTTP para eWRC con:
    - Rate limiting (1 req/s)
    - Cache de HTML en data/raw/ewrc/
    - Timeout y reintentos basicos
    """

    def __init__(self, use_cache: bool = True, delay: float = REQUEST_DELAY_S):
        self.use_cache = use_cache
        self.delay = delay
        self._last_request_time: float = 0.0
        RAW_DIR.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, url: str) -> Path:
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        return RAW_DIR / f"{url_hash}.html"

    def fetch(self, url: str) -> Optional[BeautifulSoup]:
        """
        Descarga una pagina HTML y devuelve BeautifulSoup.
        Usa cache local si esta disponible.
        """
        cache_path = self._cache_path(url)

        # Intentar desde cache
        if self.use_cache and cache_path.exists():
            logger.info("Cache hit: %s", url)
            html = cache_path.read_text(encoding="utf-8")
            return BeautifulSoup(html, "html.parser")

        # Rate limiting
        elapsed = time.time() - self._last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        logger.info("Fetching: %s", url)
        try:
            with httpx.Client(headers=HEADERS, timeout=15, follow_redirects=True) as client:
                response = client.get(url)
                self._last_request_time = time.time()

                if response.status_code != 200:
                    logger.warning("HTTP %d para %s", response.status_code, url)
                    return None

                html = response.text

                # Guardar en cache
                if self.use_cache:
                    cache_path.write_text(html, encoding="utf-8")
                    logger.debug("Cache saved: %s", cache_path.name)

                return BeautifulSoup(html, "html.parser")

        except httpx.RequestError as e:
            logger.error("Error de red en %s: %s", url, e)
            return None


# ── Parsers ───────────────────────────────────────────────────────────────────

def parse_itinerary(soup: BeautifulSoup, event_id: int) -> pd.DataFrame:
    """
    Parsea la pagina de itinerario de eWRC.

    HTML esperado (estructura eWRC):
      .harm-main
        div.text-muted  <- separador de leg
        div.harm.d-flex
          div.harm-ss   <- numero etapa (SS1, SS2...)
          div.harm-stage <- nombre etapa
          div.harm-km    <- distancia (ej: "18.55 km")
    """
    rows = []
    stage_id_counter = 1
    leg_counter = 0  # Se incrementa al encontrar el primer text-muted

    container = soup.select_one(".harm-main")
    if not container:
        # Fallback: buscar tabla de itinerario alternativa
        logger.warning("No se encontro .harm-main en el itinerario")
        return pd.DataFrame()

    items = container.find_all(["div"], recursive=False)

    for item in items:
        classes = item.get("class", [])

        # Separador de leg/jornada
        if "text-muted" in classes:
            leg_counter += 1
            continue

        # Fila de etapa
        if "harm" in classes and "d-flex" in classes:
            ss_div = item.select_one("div.harm-ss")
            name_div = item.select_one("div.harm-stage")
            km_div = item.select_one("div.harm-km")

            if not ss_div:
                continue

            stage_code = ss_div.get_text(strip=True)

            # Ignorar service parks y entradas que no son SS
            if not stage_code.upper().startswith("SS"):
                continue

            name = name_div.get_text(strip=True) if name_div else ""
            km_text = km_div.get_text(strip=True) if km_div else "0"
            distance_km = _parse_km(km_text)

            rows.append({
                "stage_id": event_id * 1000 + stage_id_counter,
                "stage_code": stage_code,
                "name": name,
                "distance_km": distance_km,
                "surface": _infer_surface(name),
                "leg_name": f"Leg {leg_counter}",
                "status": "Completed",
            })
            stage_id_counter += 1

    df = pd.DataFrame(rows)
    logger.info("Itinerario: %d etapas parseadas", len(df))
    return df


def parse_final_results(soup: BeautifulSoup, event_id: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parsea la pagina de resultados finales de eWRC.

    Devuelve (entries_df, overall_df).

    HTML esperado:
      div.final-results > table.results
        tr
          td.final-results-number  <- posicion
          td.final-entry           <- piloto (con link a entry info)
          td                       <- fabricante / coche
          td.font-weight-bold      <- tiempo total
          td                       <- gap al lider
    """
    entries_rows = []
    overall_rows = []

    # Intentar selector nuevo (post-2022)
    table = soup.select_one("div.final-results table.results")
    if not table:
        # Fallback: primera tabla con clase results
        table = soup.select_one("table.results")
    if not table:
        logger.warning("No se encontro tabla de resultados finales")
        return pd.DataFrame(), pd.DataFrame()

    rows = table.find_all("tr")
    entry_id_counter = 1
    last_stage_id = event_id * 1000 + 999  # placeholder; se sobreescribe con stages reales

    for tr in rows:
        # Saltar cabecera
        if tr.find("th"):
            continue

        entry_td = tr.select_one("td.final-entry")
        if not entry_td:
            continue

        # Extraer datos del piloto
        driver_text = entry_td.get_text(separator=" ", strip=True)
        # Formato tipico: "Ogier S. - Landais V." o "Ogier Sebastien - Landais Vincent"
        driver_name, codriver_name = _split_driver_codriver(driver_text)

        # Car number (primera celda)
        first_td = tr.find("td")
        car_number = first_td.get_text(strip=True).lstrip("#").strip() if first_td else ""

        # Fabricante/coche (celda con nombre de coche)
        manufacturer, car_model = _extract_manufacturer(tr)

        # Posicion
        pos_td = tr.select_one("td.final-results-number")
        position_text = pos_td.get_text(strip=True) if pos_td else ""
        try:
            position = int(re.sub(r"[^\d]", "", position_text))
        except (ValueError, TypeError):
            position = entry_id_counter

        # Tiempo total
        time_td = tr.select_one("td.font-weight-bold.text-left")
        if not time_td:
            # Fallback: buscar td con formato de tiempo HH:MM:SS
            time_td = _find_time_td(tr)

        total_time_s, total_time_str = _parse_time_cell(time_td)

        # Gap al lider
        gap_td = _find_gap_td(tr)
        diff_first_s, _ = _parse_gap_cell(gap_td)

        # Categoria
        cat_td = tr.select_one("td.fs-091")
        group = cat_td.get_text(strip=True) if cat_td else "WRC"

        # Retired?
        ret_stage = tr.select_one("td.final-results-stage")
        status = "Retired" if ret_stage else "Completed"

        entry_id = event_id * 100 + entry_id_counter

        entries_rows.append({
            "entry_id": entry_id,
            "driver_name": driver_name,
            "driver_code": _make_driver_code(driver_name),
            "driver_nationality": "",
            "codriver_name": codriver_name,
            "manufacturer": manufacturer,
            "car_number": car_number,
            "group": group,
        })

        if status == "Completed":
            overall_rows.append({
                "event_id": event_id,
                "stage_id": last_stage_id,
                "entry_id": entry_id,
                "position": position,
                "total_time_ms": int(total_time_s * 1000) if total_time_s else None,
                "total_time_s": total_time_s,
                "total_time_str": total_time_str,
                "diff_first_ms": int(diff_first_s * 1000) if diff_first_s is not None else None,
                "diff_first_s": diff_first_s,
                "status": status,
                "stage_code": "FINAL",
            })

        entry_id_counter += 1

    entries_df = pd.DataFrame(entries_rows)
    overall_df = pd.DataFrame(overall_rows)
    logger.info(
        "Final results: %d pilotos, %d en clasificacion",
        len(entries_df), len(overall_df)
    )
    return entries_df, overall_df


def parse_stage_times(soup: BeautifulSoup, event_id: int, stages_df: pd.DataFrame) -> pd.DataFrame:
    """
    Parsea la pagina de tiempos de etapa (/times/{id}-{slug}/).

    La pagina muestra una tabla con todos los pilotos y sus tiempos por etapa.
    Estructura tipica:
      table.results (o tabla principal)
        thead: | Driver | SS1 | SS2 | ... | SSN |
        tbody:
          tr: | Ogier | 13:54.5 | 12:10.3 | ... |

    Devuelve DataFrame con columnas compatibles con V1:
      event_id, stage_id, entry_id, position, time_s, time_str,
      diff_first_s, diff_prev_s, status, stage_code
    """
    rows = []

    # Buscar la tabla de tiempos
    table = _find_times_table(soup)
    if table is None:
        logger.warning("No se encontro tabla de tiempos de etapa")
        return pd.DataFrame()

    # Extraer cabeceras (stage codes)
    thead = table.find("thead")
    if not thead:
        logger.warning("Tabla de tiempos sin thead")
        return pd.DataFrame()

    headers = [th.get_text(strip=True) for th in thead.find_all("th")]
    # Filtrar cabeceras que son stage codes (SS1, SS2, etc.)
    stage_cols = [(i, h) for i, h in enumerate(headers) if h.upper().startswith("SS")]

    if not stage_cols:
        logger.warning("No se encontraron columnas de etapa en la tabla de tiempos")
        return pd.DataFrame()

    logger.info("Columnas de etapa encontradas: %s", [h for _, h in stage_cols])

    # Mapear stage_code a stage_id
    stage_code_to_id = {}
    if not stages_df.empty and "stage_code" in stages_df.columns:
        stage_code_to_id = dict(zip(stages_df["stage_code"], stages_df["stage_id"]))

    # Parsear filas
    tbody = table.find("tbody") or table
    data_rows = tbody.find_all("tr")

    entry_id_counter = 1

    for tr in data_rows:
        if tr.find("th"):
            continue

        cells = tr.find_all("td")
        if len(cells) < 2:
            continue

        # Primera celda: piloto (puede incluir numero de coche)
        driver_cell = cells[0]
        driver_text = driver_cell.get_text(separator=" ", strip=True)
        if not driver_text or driver_text.isdigit():
            continue

        entry_id = event_id * 100 + entry_id_counter

        # Extraer tiempo de cada etapa
        for col_idx, stage_code in stage_cols:
            if col_idx >= len(cells):
                continue

            cell = cells[col_idx]
            time_text = cell.get_text(strip=True)

            if not time_text or time_text in ("-", "DNS", "DNF", "OTL", ""):
                continue

            time_s, time_str = _parse_stage_time_text(time_text)
            if time_s is None:
                continue

            stage_id = stage_code_to_id.get(stage_code, event_id * 1000)

            rows.append({
                "event_id": event_id,
                "stage_id": stage_id,
                "entry_id": entry_id,
                "position": 0,  # Se calcula post-parse
                "time_ms": int(time_s * 1000),
                "time_s": time_s,
                "time_str": time_str,
                "diff_first_ms": None,  # Se calcula post-parse
                "diff_first_s": None,
                "diff_prev_ms": None,
                "diff_prev_s": None,
                "status": "Completed",
                "stage_code": stage_code,
            })

        entry_id_counter += 1

    df = pd.DataFrame(rows)
    if not df.empty:
        df = _calculate_positions_and_gaps(df)

    logger.info("Stage times: %d filas parseadas", len(df))
    return df


# ── Orchestrador principal ────────────────────────────────────────────────────

def scrape_event(
    event_id: int,
    slug: str,
    client: Optional[EwrcClient] = None,
    wrc_only: bool = True,
) -> dict[str, pd.DataFrame]:
    """
    Descarga y parsea un evento completo de eWRC.

    Devuelve dict con DataFrames listos para guardar como CSV:
      {
        "stages": pd.DataFrame,
        "entries": pd.DataFrame,
        "overall": pd.DataFrame,
        "stage_times": pd.DataFrame,
      }
    """
    if client is None:
        client = EwrcClient()

    results: dict[str, pd.DataFrame] = {}

    # 1. Itinerario (etapas)
    itinerary_url = f"{BASE_URL}/event/{event_id}-{slug}/itinerary"
    soup = client.fetch(itinerary_url)
    if soup:
        results["stages"] = parse_itinerary(soup, event_id)
    else:
        logger.error("No se pudo descargar itinerario de %s", slug)
        results["stages"] = pd.DataFrame()

    # 2. Resultados finales (pilotos + clasificacion final)
    final_url = f"{BASE_URL}/event/{event_id}-{slug}/final-results"
    soup = client.fetch(final_url)
    if soup:
        entries_df, overall_df = parse_final_results(soup, event_id)
        results["entries"] = entries_df
        results["overall"] = overall_df
    else:
        logger.error("No se pudo descargar resultados finales de %s", slug)
        results["entries"] = pd.DataFrame()
        results["overall"] = pd.DataFrame()

    # 3. Tiempos de etapa
    times_url = f"{BASE_URL}/times/{event_id}-{slug}/"
    soup = client.fetch(times_url)
    if soup:
        results["stage_times"] = parse_stage_times(
            soup, event_id, results.get("stages", pd.DataFrame())
        )
    else:
        logger.warning("No se pudo descargar stage times de %s", slug)
        results["stage_times"] = pd.DataFrame()

    return results


def parse_final_results_v2(
    soup: BeautifulSoup, event_id: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parsea la página /event/{id}-{slug}/final-results del ewrc ACTUAL (Next.js/Tailwind).

    La página usa SSR y renderiza una <table> con filas en pares:
      Fila impar:  (pos+car_num) | (driver+codriver) | category | total_time | gap
      Fila par:    car_model (colspan)

    Para pilotos retirados, la celda de posición contiene el stage de abandono
    (e.g., <span data-i18n="lg_stage">SS</span>16) en lugar del número de posición.
    """
    entries_rows: list[dict] = []
    overall_rows: list[dict] = []

    table = soup.find("table")
    if not table:
        logger.warning("parse_final_results_v2: no se encontro <table>")
        return pd.DataFrame(), pd.DataFrame()

    rows = table.find_all("tr")
    entry_id_counter = 1
    pos_counter = 1

    i = 0
    while i < len(rows):
        main_row = rows[i]
        cells = main_row.find_all("td")

        if len(cells) != 5:
            i += 1
            continue

        # ── Celda 0: posicion + numero de coche ──────────────────────────────
        pos_cell = cells[0]
        pos_text = pos_cell.get_text(separator="|", strip=True)
        nums = re.findall(r"\d+", pos_text)

        # Detectar si es retirado: la celda tiene el patron SS\d+
        stage_span = pos_cell.find("span", attrs={"data-i18n": "lg_stage"})
        is_retired = stage_span is not None
        retirement_stage = None
        if is_retired and len(nums) >= 1:
            retirement_stage = f"SS{nums[0]}"
            position = None
        else:
            position = int(nums[0]) if nums else pos_counter
            pos_counter += 1

        car_num = nums[1] if len(nums) >= 2 else (nums[0] if nums else "")

        # ── Celda 1: piloto + copiloto ───────────────────────────────────────
        driver_cell = cells[1]
        driver_parts = driver_cell.get_text(separator="|", strip=True).split("|")
        # Formato: short_name | full_name | co_short | co_full  (o variaciones)
        driver_short = driver_parts[0] if driver_parts else ""
        driver_full = driver_parts[1] if len(driver_parts) > 1 else driver_short
        codriver_short = driver_parts[2] if len(driver_parts) > 2 else ""
        codriver_full = driver_parts[3] if len(driver_parts) > 3 else codriver_short

        # ── Celda 2: categoria ───────────────────────────────────────────────
        group = cells[2].get_text(strip=True)

        # ── Celda 3: tiempo total ────────────────────────────────────────────
        time_text = cells[3].get_text(strip=True)
        # Limpiar penalizaciones como "[SR]", "0:30"
        time_clean = re.sub(r"\[.*?\]", "", time_text).strip()
        # Extraer solo el tiempo principal (primer patron H:MM:SS o MM:SS)
        time_match = re.search(r"\d+:\d{2}:\d{2}\.?\d*", time_clean)
        if time_match:
            time_clean = time_match.group(0)
        total_time_s, total_time_str = _parse_time_text(time_clean)

        # ── Celda 4: gap ─────────────────────────────────────────────────────
        gap_text = cells[4].get_text(separator="|", strip=True)
        # El gap aparece duplicado: '+18.5|+|18.5' → tomar el primer valor
        gap_match = re.search(r"\+?([\d:]+\.?\d*)", gap_text)
        if gap_match and position != 1:
            diff_str = gap_match.group(1)
            # Puede ser segundos simples o minutos:segundos
            if ":" in diff_str:
                diff_s, _ = _parse_time_text(diff_str)
            else:
                try:
                    diff_s = float(diff_str)
                except ValueError:
                    diff_s = None
        else:
            diff_s = 0.0

        # ── Modelo de coche (fila par siguiente) ─────────────────────────────
        car_model = ""
        if i + 1 < len(rows):
            next_row_cells = rows[i + 1].find_all("td")
            if len(next_row_cells) == 1:
                car_model = next_row_cells[0].get_text(strip=True)

        # ── Fabricante ───────────────────────────────────────────────────────
        manufacturer = _manufacturer_from_car_model(car_model)

        entry_id = event_id * 100 + entry_id_counter

        entries_rows.append({
            "entry_id": entry_id,
            "driver_name": driver_full or driver_short,
            "driver_code": _make_driver_code(driver_full or driver_short),
            "driver_nationality": "",
            "codriver_name": codriver_full or codriver_short,
            "manufacturer": manufacturer,
            "car_number": car_num,
            "car_model": car_model,
            "group": group,
        })

        status = "Retired" if is_retired else "Completed"
        if not is_retired and total_time_s is not None:
            overall_rows.append({
                "event_id": event_id,
                "stage_id": event_id * 1000 + 999,
                "entry_id": entry_id,
                "position": position,
                "total_time_ms": int(total_time_s * 1000),
                "total_time_s": total_time_s,
                "total_time_str": total_time_str,
                "diff_first_ms": int(diff_s * 1000) if diff_s is not None else None,
                "diff_first_s": diff_s,
                "status": status,
                "stage_code": "FINAL",
                "retirement_stage": retirement_stage,
            })

        entry_id_counter += 1
        # Avanzar 2 filas si hay fila de modelo, si no 1
        i += 2 if car_model else 1

    entries_df = pd.DataFrame(entries_rows)
    overall_df = pd.DataFrame(overall_rows)
    logger.info(
        "parse_final_results_v2: %d entradas, %d en clasificacion",
        len(entries_df), len(overall_df),
    )
    return entries_df, overall_df


def parse_stages_minimal(event_id: int, n_stages: int) -> pd.DataFrame:
    """
    Genera un DataFrame mínimo de etapas cuando no hay datos de itinerario disponibles.
    Usa el número de etapas conocido (del HTML de final-results o valor hardcoded).
    """
    rows = []
    for n in range(1, n_stages + 1):
        rows.append({
            "stage_id": event_id * 1000 + n,
            "stage_code": f"SS{n}",
            "name": f"Special Stage {n}",
            "distance_km": 0.0,
            "surface": "Unknown",
            "leg_name": f"Leg {(n - 1) // 4 + 1}",
            "status": "Completed",
        })
    return pd.DataFrame(rows)


def _manufacturer_from_car_model(car_model: str) -> str:
    """Extrae el fabricante del nombre del modelo de coche."""
    for mfr in ["Toyota", "Hyundai", "Ford", "Citroen", "Citroën", "Skoda", "Škoda",
                "M-Sport", "Peugeot", "Volkswagen", "Subaru", "Mitsubishi"]:
        if mfr.lower() in car_model.lower():
            return mfr
    return car_model.split()[0] if car_model else ""


def save_results(results: dict[str, pd.DataFrame], slug: str) -> None:
    """Guarda los DataFrames como CSVs en data/processed/ (misma estructura que V1)."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    safe_slug = slug.replace("-", "_")

    file_map = {
        "stages": f"{safe_slug}_stages.csv",
        "entries": f"{safe_slug}_entries.csv",
        "overall": f"{safe_slug}_overall.csv",
        "stage_times": f"{safe_slug}_stage_times.csv",
    }

    for key, filename in file_map.items():
        df = results.get(key, pd.DataFrame())
        if df.empty:
            logger.warning("DataFrame vacio para %s — no se guarda", key)
            continue
        path = PROCESSED_DIR / filename
        df.to_csv(path, index=False, encoding="utf-8-sig")
        logger.info("Guardado: %s (%d filas)", filename, len(df))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_km(text: str) -> float:
    """Extrae distancia en km de texto como '18.55 km' o '18,55'."""
    text = text.replace(",", ".").replace("km", "").strip()
    try:
        return float(text)
    except ValueError:
        return 0.0


def _infer_surface(stage_name: str) -> str:
    """Infiere la superficie de la etapa por el nombre del rally/etapa."""
    name_lower = stage_name.lower()
    if any(w in name_lower for w in ["snow", "nieve", "ice", "hielo"]):
        return "Snow"
    if any(w in name_lower for w in ["gravel", "grava", "tierra"]):
        return "Gravel"
    return "Tarmac"


def _split_driver_codriver(text: str) -> tuple[str, str]:
    """
    Divide 'Ogier S. - Landais V.' en ('Ogier S.', 'Landais V.').
    Maneja varios separadores.
    """
    for sep in [" - ", " / ", "/"]:
        if sep in text:
            parts = text.split(sep, 1)
            return parts[0].strip(), parts[1].strip()
    return text.strip(), ""


def _make_driver_code(name: str) -> str:
    """Genera codigo de 3 letras del apellido del piloto."""
    parts = name.strip().split()
    if not parts:
        return ""
    return parts[0][:3].upper()


def _extract_manufacturer(tr) -> tuple[str, str]:
    """Extrae fabricante y modelo del coche de una fila de resultados."""
    # Buscar celda con nombre de coche (Toyota GR Yaris, Hyundai i20 N, Ford Puma, etc.)
    car_cell = tr.select_one("td.font-weight-bold.lh-130")
    if car_cell:
        full_text = car_cell.get_text(strip=True)
        # Fabricantes conocidos WRC
        for mfr in ["Toyota", "Hyundai", "Ford", "M-Sport"]:
            if mfr.lower() in full_text.lower():
                return mfr, full_text
        return full_text, full_text

    # Fallback: buscar cualquier celda con fabricantes conocidos
    for td in tr.find_all("td"):
        text = td.get_text(strip=True)
        for mfr in ["Toyota", "Hyundai", "Ford", "M-Sport"]:
            if mfr.lower() in text.lower():
                return mfr, text

    return "", ""


def _parse_time_cell(td) -> tuple[Optional[float], Optional[str]]:
    """
    Parsea una celda de tiempo.
    Formatos: '3:19:06.1', '13:54.5', '1h 23m 45.6s'
    """
    if not td:
        return None, None
    text = td.get_text(strip=True)
    return _parse_time_text(text)


def _parse_time_text(text: str) -> tuple[Optional[float], Optional[str]]:
    """
    Convierte string de tiempo a (segundos, string_formateado).
    Acepta: 'H:MM:SS.t', 'MM:SS.t', 'HH:MM:SS'
    """
    text = text.strip()
    if not text or text in ("-", "DNS", "DNF", "OTL", "Retired"):
        return None, None

    # Formato H:MM:SS.t (tiempo total de rally: 3:19:06.1)
    m = re.match(r"^(\d+):(\d{2}):(\d{2})\.?(\d*)$", text)
    if m:
        h, mn, s, dec = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        total = h * 3600 + mn * 60 + s + (float(f"0.{dec}") if dec else 0)
        return round(total, 1), text

    # Formato MM:SS.t (tiempo por etapa: 13:54.5)
    m = re.match(r"^(\d{1,2}):(\d{2})\.?(\d*)$", text)
    if m:
        mn, s, dec = int(m.group(1)), int(m.group(2)), m.group(3)
        total = mn * 60 + s + (float(f"0.{dec}") if dec else 0)
        return round(total, 1), text

    return None, None


def _parse_stage_time_text(text: str) -> tuple[Optional[float], Optional[str]]:
    """Alias para tiempos de etapa."""
    return _parse_time_text(text)


def _parse_gap_cell(td) -> tuple[Optional[float], Optional[str]]:
    """Parsea celda de gap: '+18.5', '0', '-'."""
    if not td:
        return 0.0, "0"
    text = td.get_text(strip=True).lstrip("+")
    if not text or text in ("-", "0"):
        return 0.0, "0"
    try:
        return float(text), text
    except ValueError:
        return None, None


def _find_time_td(tr):
    """Busca la celda de tiempo total en una fila de resultados."""
    for td in tr.find_all("td"):
        text = td.get_text(strip=True)
        if re.match(r"^\d+:\d{2}:\d{2}", text):
            return td
    return None


def _find_gap_td(tr):
    """Busca la celda de gap al lider en una fila de resultados."""
    tds = tr.find_all("td")
    for i, td in enumerate(tds):
        text = td.get_text(strip=True)
        if re.match(r"^\+\d+", text):
            return td
    return None


def _find_times_table(soup: BeautifulSoup):
    """
    Busca la tabla principal de tiempos de etapa en la pagina /times/.
    Intenta varios selectores para ser resiliente a cambios de HTML.
    """
    # Selector 1: tabla con clase results y thead con SS
    for table in soup.find_all("table"):
        thead = table.find("thead")
        if thead:
            headers = [th.get_text(strip=True) for th in thead.find_all("th")]
            if any(h.upper().startswith("SS") for h in headers):
                return table

    # Selector 2: primera tabla grande de la pagina
    tables = soup.find_all("table")
    if tables:
        # Preferir la tabla con mas columnas
        return max(tables, key=lambda t: len(t.find_all("th")), default=None)

    return None


def _calculate_positions_and_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula posicion y gap al lider por etapa.
    Ordena por time_s dentro de cada stage_id.
    """
    result_parts = []

    for stage_id, group in df.groupby("stage_id"):
        group = group.sort_values("time_s").reset_index(drop=True)
        group["position"] = range(1, len(group) + 1)
        leader_time = group.iloc[0]["time_s"]
        group["diff_first_s"] = (group["time_s"] - leader_time).round(3)
        group["diff_first_ms"] = (group["diff_first_s"] * 1000).astype(int)
        group["diff_prev_s"] = group["diff_first_s"].diff().fillna(0).round(3)
        group["diff_prev_ms"] = (group["diff_prev_s"] * 1000).astype(int)
        result_parts.append(group)

    if result_parts:
        return pd.concat(result_parts, ignore_index=True)
    return df
