"""
Scraper Playwright para eWRC-results.com (Bloque 11).

Playwright ejecuta un navegador headless real, espera el render JS
completo y extrae los tiempos de etapa que BeautifulSoup no podia ver.

Instalacion previa (una vez):
    pip install playwright
    playwright install chromium

Uso:
    python -m ingestion.playwright_scraper
    python -m ingestion.playwright_scraper --event-id 89918 --slug rallye-automobile-monte-carlo-2025
    python -m ingestion.playwright_scraper --no-cache
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import logging
import time
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────

BASE_URL = "https://ewrc-results.com"

# WRC 2025 — eventos con sus IDs de eWRC
WRC_2025_EVENTS = [
    (89918,  "rallye-automobile-monte-carlo-2025"),
    (90090,  "rally-sweden-2025"),
    (91205,  "rally-guanajuato-mexico-2025"),
    (91206,  "safari-rally-kenya-2025"),
    (91207,  "croatia-rally-2025"),
    (91208,  "rally-de-portugal-2025"),
    (91209,  "rally-italia-sardegna-2025"),
    (91210,  "rally-poland-2025"),
]

REQUEST_DELAY_S = 1.5  # Rate limiting etico (algo mas generoso que httpx)

# ── Paths ─────────────────────────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR       = _PROJECT_ROOT / "data" / "raw" / "ewrc_playwright"
PROCESSED_DIR = _PROJECT_ROOT / "data" / "processed"


def _cache_path(url: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
    return RAW_DIR / f"{url_hash}.html"


# ── Playwright scraper ────────────────────────────────────────────────────────

async def _fetch_page(url: str, use_cache: bool = True) -> Optional[str]:
    """
    Descarga una pagina con Playwright esperando el render JS completo.
    Cachea el HTML resultante en data/raw/ewrc_playwright/.
    """
    cache = _cache_path(url)

    if use_cache and cache.exists():
        logger.info("Cache hit: %s", url)
        return cache.read_text(encoding="utf-8")

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        logger.error(
            "Playwright no instalado. Ejecuta:\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        )
        return None

    logger.info("Fetching (Playwright): %s", url)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page    = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=30_000)
            # Esperar a que la tabla principal este visible
            try:
                await page.wait_for_selector("table", timeout=15_000)
            except Exception:
                logger.warning("Timeout esperando tabla en %s", url)

            html = await page.content()
            await asyncio.sleep(REQUEST_DELAY_S)

            if use_cache:
                cache.write_text(html, encoding="utf-8")
                logger.debug("Cache guardado: %s", cache.name)

            return html
        finally:
            await browser.close()


def _parse_stage_times_html(html: str, event_id: int,
                             stages_df: pd.DataFrame) -> pd.DataFrame:
    """
    Parsea la tabla de tiempos de etapa del HTML renderizado por Playwright.

    La pagina /stage-times de eWRC (Next.js) muestra una tabla con:
      - Columna 0: posicion + piloto (o solo piloto en algunas vistas)
      - Columnas 1..N: SS1, SS2, ..., SSN

    Devuelve DataFrame compatible con *_stage_times.csv de V2.
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        logger.error("beautifulsoup4 no instalado.")
        return pd.DataFrame()

    soup  = BeautifulSoup(html, "html.parser")
    rows  = []

    # Buscar la tabla principal (la que tiene cabeceras de tipo SS1, SS2...)
    table = None
    for t in soup.find_all("table"):
        headers = [th.get_text(strip=True) for th in t.find_all("th")]
        if any(h.upper().startswith("SS") for h in headers):
            table = t
            break

    if not table:
        logger.warning("No se encontro tabla de stage times en el HTML")
        return pd.DataFrame()

    # Extraer cabeceras → stage codes
    headers    = [th.get_text(strip=True) for th in table.find_all("th")]
    stage_cols = [(i, h) for i, h in enumerate(headers) if h.upper().startswith("SS")]

    # Mapeo stage_code → stage_id
    sc_to_id: dict[str, int] = {}
    if not stages_df.empty and "stage_code" in stages_df.columns:
        sc_to_id = dict(zip(stages_df["stage_code"], stages_df["stage_id"]))

    tbody     = table.find("tbody") or table
    entry_ctr = 1

    for tr in tbody.find_all("tr"):
        if tr.find("th"):
            continue
        cells = tr.find_all("td")
        if len(cells) < 2:
            continue

        # Primera celda: piloto
        driver_text = cells[0].get_text(separator=" ", strip=True)
        if not driver_text:
            continue

        entry_id = event_id * 100 + entry_ctr

        for col_idx, stage_code in stage_cols:
            if col_idx >= len(cells):
                continue
            time_text = cells[col_idx].get_text(strip=True)
            if not time_text or time_text in ("-", "DNS", "DNF", "OTL", ""):
                continue

            time_s, time_str = _parse_time(time_text)
            if time_s is None:
                continue

            stage_id = sc_to_id.get(stage_code, event_id * 1000)
            rows.append({
                "event_id":      event_id,
                "stage_id":      stage_id,
                "entry_id":      entry_id,
                "position":      0,       # se recalcula abajo
                "time_ms":       int(time_s * 1000),
                "time_s":        time_s,
                "time_str":      time_str,
                "diff_first_ms": None,
                "diff_first_s":  None,
                "diff_prev_ms":  None,
                "diff_prev_s":   None,
                "status":        "Completed",
                "stage_code":    stage_code,
            })

        entry_ctr += 1

    df = pd.DataFrame(rows)
    if not df.empty:
        df = _calculate_positions(df)
    logger.info("Stage times parseados: %d filas", len(df))
    return df


def _parse_time(text: str):
    import re
    text = text.strip()
    if not text or text in ("-", "DNS", "DNF", "OTL", "Retired"):
        return None, None
    m = re.match(r"^(\d+):(\d{2}):(\d{2})\.?(\d*)$", text)
    if m:
        h, mn, s, dec = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        total = h * 3600 + mn * 60 + s + (float(f"0.{dec}") if dec else 0)
        return round(total, 1), text
    m = re.match(r"^(\d{1,2}):(\d{2})\.?(\d*)$", text)
    if m:
        mn, s, dec = int(m.group(1)), int(m.group(2)), m.group(3)
        total = mn * 60 + s + (float(f"0.{dec}") if dec else 0)
        return round(total, 1), text
    return None, None


def _calculate_positions(df: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for stage_id, grp in df.groupby("stage_id"):
        grp   = grp.sort_values("time_s").reset_index(drop=True)
        grp["position"]      = range(1, len(grp) + 1)
        leader               = grp.iloc[0]["time_s"]
        grp["diff_first_s"]  = (grp["time_s"] - leader).round(3)
        grp["diff_first_ms"] = (grp["diff_first_s"] * 1000).astype(int)
        grp["diff_prev_s"]   = grp["diff_first_s"].diff().fillna(0).round(3)
        grp["diff_prev_ms"]  = (grp["diff_prev_s"] * 1000).astype(int)
        parts.append(grp)
    return pd.concat(parts, ignore_index=True) if parts else df


# ── Orchestrador ──────────────────────────────────────────────────────────────

async def scrape_event_stage_times(
    event_id: int,
    slug: str,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Descarga y parsea los tiempos de etapa de un evento completo.
    Solo añade stage_times que faltan (no sobreescribe los ya existentes).
    """
    url = f"{BASE_URL}/event/{event_id}-{slug}/stage-times"

    # Cargar stages existentes para mapear stage_code → stage_id
    safe_slug = slug.replace("-", "_")
    stages_path = PROCESSED_DIR / f"{safe_slug}_stages.csv"
    stages_df   = pd.DataFrame()
    if stages_path.exists():
        stages_df = pd.read_csv(stages_path, encoding="utf-8-sig")

    html = await _fetch_page(url, use_cache=use_cache)
    if not html:
        return pd.DataFrame()

    return _parse_stage_times_html(html, event_id, stages_df)


def save_stage_times(df: pd.DataFrame, slug: str) -> None:
    """Guarda stage_times CSV en data/processed/."""
    if df.empty:
        logger.warning("Sin datos de stage times para %s", slug)
        return
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    safe_slug = slug.replace("-", "_")
    path = PROCESSED_DIR / f"{safe_slug}_stage_times.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    logger.info("Guardado: %s (%d filas)", path.name, len(df))


async def run(event_id: Optional[int] = None, slug: Optional[str] = None,
              use_cache: bool = True) -> None:
    targets = [(event_id, slug)] if event_id and slug else WRC_2025_EVENTS
    for ev_id, ev_slug in targets:
        logger.info("--- %s (ID: %d) ---", ev_slug, ev_id)
        df = await scrape_event_stage_times(ev_id, ev_slug, use_cache=use_cache)
        if not df.empty:
            save_stage_times(df, ev_slug)
        else:
            logger.warning("Sin datos para %s", ev_slug)
        time.sleep(REQUEST_DELAY_S)


def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        datefmt="%H:%M:%S")
    parser = argparse.ArgumentParser(description="Playwright scraper para eWRC stage times")
    parser.add_argument("--event-id", type=int, default=None)
    parser.add_argument("--slug",     type=str, default=None)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()
    asyncio.run(run(args.event_id, args.slug, use_cache=not args.no_cache))


if __name__ == "__main__":
    main()
