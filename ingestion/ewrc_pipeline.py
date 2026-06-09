"""
Pipeline de ingesta V2 — datos reales desde eWRC-results.com y Wikipedia.

Estrategia por evento:
  1. ewrc.com /final-results (SSR) → entries + overall (funciona en TODOS los eventos)
  2. Wikipedia REST API v1        → stages + stage_times + entries/overall alternativos
  3. Fallback minimal             → stages generados desde el count de etapas

Uso:
    python -m ingestion.ewrc_pipeline
    python -m ingestion.ewrc_pipeline --event-id 89918 --slug rallye-automobile-monte-carlo-2025
    python -m ingestion.ewrc_pipeline --no-cache  # fuerza re-descarga
"""

from __future__ import annotations

import argparse
import logging
import sys

import pandas as pd

from ingestion.ewrc_scraper import (
    EwrcClient,
    WRC_2025_EVENTS,
    parse_final_results_v2,
    parse_stages_minimal,
    save_results,
    BASE_URL,
    HEADERS,
)
from ingestion.wikipedia_scraper import (
    WikiClient,
    SLUG_TO_WIKI,
    scrape_wiki_event,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s -- %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ingestion.ewrc_pipeline")

# Número de etapas conocido por evento cuando no hay otra fuente
KNOWN_STAGE_COUNTS: dict[str, int] = {
    "rallye-automobile-monte-carlo-2025": 15,
    "rally-sweden-2025": 14,
    "safari-rally-kenya-2025": 17,
    "rally-de-portugal-2025": 18,
    "rally-finland-2025": 23,
    "rally-chile-2025": 21,
    "central-european-rally-2025": 17,
    "rally-japan-2025": 19,
}

# Superficie por defecto por rally
DEFAULT_SURFACE: dict[str, str] = {
    "rallye-automobile-monte-carlo-2025": "Tarmac",
    "rally-sweden-2025": "Snow",
    "safari-rally-kenya-2025": "Gravel",
    "rally-de-portugal-2025": "Gravel",
    "rally-finland-2025": "Gravel",
    "rally-chile-2025": "Gravel",
    "central-european-rally-2025": "Tarmac",
    "rally-japan-2025": "Tarmac",
}


def scrape_ewrc_event(
    event_id: int,
    slug: str,
    ewrc_client: EwrcClient,
) -> dict[str, pd.DataFrame]:
    """
    Obtiene entries + overall desde ewrc.com /final-results (página con SSR).
    Devuelve dict parcial con las claves disponibles.
    """
    final_url = f"{BASE_URL}/event/{event_id}-{slug}/final-results"
    soup = ewrc_client.fetch(final_url)

    if soup is None:
        logger.warning("ewrc: no se pudo descargar final-results de %s", slug)
        return {}

    entries_df, overall_df = parse_final_results_v2(soup, event_id)

    results: dict[str, pd.DataFrame] = {}
    if not entries_df.empty:
        results["entries"] = entries_df
    if not overall_df.empty:
        results["overall"] = overall_df

    return results


def run(event_id: int | None = None, slug: str | None = None, use_cache: bool = True) -> None:
    """Punto de entrada del pipeline eWRC."""
    logger.info("=== Rally Performance Analyzer V2 -- Pipeline Híbrido ===")

    ewrc_client = EwrcClient(use_cache=use_cache)
    wiki_client = WikiClient(use_cache=use_cache)

    if event_id and slug:
        targets = [(event_id, slug)]
    else:
        targets = WRC_2025_EVENTS

    success_count = 0

    for ev_id, ev_slug in targets:
        logger.info("--- Procesando evento %d (%s) ---", ev_id, ev_slug)
        try:
            results: dict[str, pd.DataFrame] = {}

            # ── 1. Fuente ewrc.com (entries + overall) ────────────────────────
            ewrc_data = scrape_ewrc_event(ev_id, ev_slug, ewrc_client)
            results.update(ewrc_data)

            if ewrc_data:
                logger.info("  [ewrc] entries=%d, overall=%d",
                    len(ewrc_data.get("entries", pd.DataFrame())),
                    len(ewrc_data.get("overall", pd.DataFrame())),
                )

            # ── 2. Fuente Wikipedia (stages + stage_times + complement) ───────
            if ev_slug in SLUG_TO_WIKI:
                logger.info("  Intentando Wikipedia para %s ...", ev_slug)
                wiki_data = scrape_wiki_event(ev_slug, ev_id, wiki_client)

                if wiki_data:
                    # stages y stage_times sólo vienen de Wikipedia
                    for key in ("stages", "stage_times"):
                        if key in wiki_data and not wiki_data[key].empty:
                            results[key] = wiki_data[key]
                            logger.info("  [wiki] %s: %d filas", key, len(wiki_data[key]))

                    # Para entries/overall: preferir Wikipedia si tiene más datos
                    # (ewrc puede tener event_id incorrecto devolviendo pocos resultados)
                    for key in ("entries", "overall"):
                        wiki_rows = len(wiki_data.get(key, pd.DataFrame()))
                        ewrc_rows = len(results.get(key, pd.DataFrame()))
                        if wiki_rows > ewrc_rows and wiki_rows > 0:
                            results[key] = wiki_data[key]
                            logger.info(
                                "  [wiki] %s: %d filas (vs ewrc %d)",
                                key, wiki_rows, ewrc_rows,
                            )
                        elif key not in results or ewrc_rows == 0:
                            if wiki_rows > 0:
                                results[key] = wiki_data[key]
                                logger.info("  [wiki-fallback] %s: %d filas", key, wiki_rows)
            else:
                logger.info("  Sin artículo Wikipedia para %s", ev_slug)

            # ── 3. Stages mínimas si siguen faltando ──────────────────────────
            if "stages" not in results or results.get("stages", pd.DataFrame()).empty:
                n = KNOWN_STAGE_COUNTS.get(ev_slug, 15)
                surface = DEFAULT_SURFACE.get(ev_slug, "Unknown")
                stages_df = parse_stages_minimal(ev_id, n)
                # Aplicar superficie correcta
                stages_df["surface"] = surface
                results["stages"] = stages_df
                logger.info("  [minimal] stages generadas: %d etapas (%s)", n, surface)

            # ── 4. Asegurar stage_times vacío si no existe ────────────────────
            if "stage_times" not in results:
                results["stage_times"] = pd.DataFrame()

            # ── Resumen ───────────────────────────────────────────────────────
            for key, df in results.items():
                if df.empty:
                    logger.warning("  [!] %s: sin datos", key)
                else:
                    logger.info("  [OK] %s: %d filas", key, len(df))

            if results.get("entries", pd.DataFrame()).empty and results.get("overall", pd.DataFrame()).empty:
                logger.error("  Evento %d sin datos útiles, omitiendo", ev_id)
                continue

            save_results(results, ev_slug)
            success_count += 1
            logger.info("  Evento %s guardado correctamente", ev_slug)

        except Exception as e:
            logger.error("  Error procesando %s: %s", ev_slug, e, exc_info=True)

    logger.info("=== Pipeline completado: %d/%d eventos ===", success_count, len(targets))

    if success_count == 0:
        logger.error("No se procesó ningún evento. Revisar logs.")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline de ingesta Rally Performance Analyzer")
    parser.add_argument("--event-id", type=int, default=None, help="ID del evento en eWRC")
    parser.add_argument("--slug", type=str, default=None, help="Slug del evento")
    parser.add_argument("--no-cache", action="store_true", help="Forzar re-descarga")
    args = parser.parse_args()

    if bool(args.event_id) != bool(args.slug):
        parser.error("--event-id y --slug deben usarse juntos")

    run(
        event_id=args.event_id,
        slug=args.slug,
        use_cache=not args.no_cache,
    )


if __name__ == "__main__":
    main()
