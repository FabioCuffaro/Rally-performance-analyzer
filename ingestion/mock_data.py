"""
Datos mock basados en la estructura real de la WRC Live Timing API.

Simulan el Rally Monte Carlo 2024 con 6 pilotos y 5 etapas.
Se usan cuando la API real no está accesible (red corporativa, desarrollo offline).
"""

from __future__ import annotations

# ── Temporada activa ──────────────────────────────────────────────────────────
MOCK_SEASON: dict = {
    "rallyEvents": {
        "items": [
            {
                "id": 1,
                "name": "Rallye Automobile Monte Carlo",
                "status": "Completed",
                "rally": {
                    "country": {"name": "France", "iso2": "FR", "iso3": "FRA"}
                },
                "eventDays": [
                    {"startDate": "2024-01-25T00:00:00"},
                    {"startDate": "2024-01-26T00:00:00"},
                    {"startDate": "2024-01-27T00:00:00"},
                    {"finishDate": "2024-01-28T00:00:00"},
                ],
                "winner": {"driver": {"fullName": "Sébastien Ogier"}},
            },
            {
                "id": 2,
                "name": "Rally Sweden",
                "status": "Completed",
                "rally": {
                    "country": {"name": "Sweden", "iso2": "SE", "iso3": "SWE"}
                },
                "eventDays": [
                    {"startDate": "2024-02-15T00:00:00"},
                    {"finishDate": "2024-02-18T00:00:00"},
                ],
                "winner": {"driver": {"fullName": "Elfyn Evans"}},
            },
            {
                "id": 3,
                "name": "Safari Rally Kenya",
                "status": "Completed",
                "rally": {
                    "country": {"name": "Kenya", "iso2": "KE", "iso3": "KEN"}
                },
                "eventDays": [
                    {"startDate": "2024-03-28T00:00:00"},
                    {"finishDate": "2024-03-31T00:00:00"},
                ],
                "winner": {"driver": {"fullName": "Thierry Neuville"}},
            },
        ]
    }
}

# ── Itinerario (Monte Carlo) ───────────────────────────────────────────────────
MOCK_ITINERARY: dict = {
    "rallyId": 1,
    "itineraryLegs": [
        {
            "itineraryLegId": 10,
            "name": "Leg 1",
            "startListId": 100,
            "itinerarySections": [
                {
                    "itinerarySectionId": 20,
                    "stages": [
                        {
                            "stageId": 101,
                            "code": "SS1",
                            "name": "Col de Turini",
                            "distance": 18.55,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                        {
                            "stageId": 102,
                            "code": "SS2",
                            "name": "La Cabanette - Col de Braus",
                            "distance": 12.3,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                    ],
                }
            ],
        },
        {
            "itineraryLegId": 11,
            "name": "Leg 2",
            "startListId": 101,
            "itinerarySections": [
                {
                    "itinerarySectionId": 21,
                    "stages": [
                        {
                            "stageId": 103,
                            "code": "SS3",
                            "name": "Lucéram - Lantosque",
                            "distance": 22.1,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                        {
                            "stageId": 104,
                            "code": "SS4",
                            "name": "Saint-Léger - Escragnolles",
                            "distance": 15.8,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                    ],
                }
            ],
        },
        {
            "itineraryLegId": 12,
            "name": "Leg 3",
            "startListId": 102,
            "itinerarySections": [
                {
                    "itinerarySectionId": 22,
                    "stages": [
                        {
                            "stageId": 105,
                            "code": "SS5",
                            "name": "Col de Turini (Power Stage)",
                            "distance": 18.55,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                    ],
                }
            ],
        },
    ],
}

# ── Pilotos inscritos ─────────────────────────────────────────────────────────
MOCK_ENTRIES: list[dict] = [
    {
        "entryId": 201,
        "identifier": "17",
        "driver": {"fullName": "Sébastien Ogier", "code": "OGI", "country": {"iso2": "FR"}},
        "codriver": {"fullName": "Vincent Landais"},
        "manufacturer": {"name": "Toyota"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 202,
        "identifier": "33",
        "driver": {"fullName": "Elfyn Evans", "code": "EVA", "country": {"iso2": "GB"}},
        "codriver": {"fullName": "Scott Martin"},
        "manufacturer": {"name": "Toyota"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 203,
        "identifier": "11",
        "driver": {"fullName": "Thierry Neuville", "code": "NEU", "country": {"iso2": "BE"}},
        "codriver": {"fullName": "Martijn Wydaeghe"},
        "manufacturer": {"name": "Hyundai"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 204,
        "identifier": "6",
        "driver": {"fullName": "Ott Tänak", "code": "TAN", "country": {"iso2": "EE"}},
        "codriver": {"fullName": "Martin Järveoja"},
        "manufacturer": {"name": "Hyundai"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 205,
        "identifier": "69",
        "driver": {"fullName": "Kalle Rovanperä", "code": "ROV", "country": {"iso2": "FI"}},
        "codriver": {"fullName": "Jonne Halttunen"},
        "manufacturer": {"name": "Toyota"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 206,
        "identifier": "8",
        "driver": {"fullName": "Ott Tänak", "code": "TAN", "country": {"iso2": "EE"}},
        "codriver": {"fullName": "Andreas Mikkelsen"},
        "manufacturer": {"name": "Hyundai"},
        "group": {"name": "WRC"},
    },
]

# ── Tiempos por etapa ─────────────────────────────────────────────────────────
# Formato: stage_id → lista de tiempos
# Tiempos en milisegundos, basados en ritmos reales del WRC (~1 min/km en tarmac)

MOCK_STAGE_TIMES: dict[int, list[dict]] = {
    101: [  # SS1 — Col de Turini (18.55 km) → ~14 min
        {"entryId": 201, "position": 1, "elapsedDurationMs": 834_500, "diffFirstMs": 0,     "diffPrevMs": 0,    "status": "Completed"},
        {"entryId": 202, "position": 2, "elapsedDurationMs": 836_200, "diffFirstMs": 1_700, "diffPrevMs": 1_700, "status": "Completed"},
        {"entryId": 203, "position": 3, "elapsedDurationMs": 837_800, "diffFirstMs": 3_300, "diffPrevMs": 1_600, "status": "Completed"},
        {"entryId": 205, "position": 4, "elapsedDurationMs": 839_100, "diffFirstMs": 4_600, "diffPrevMs": 1_300, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 841_000, "diffFirstMs": 6_500, "diffPrevMs": 1_900, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 844_300, "diffFirstMs": 9_800, "diffPrevMs": 3_300, "status": "Completed"},
    ],
    102: [  # SS2 — La Cabanette (12.3 km) → ~9.5 min
        {"entryId": 203, "position": 1, "elapsedDurationMs": 572_000, "diffFirstMs": 0,     "diffPrevMs": 0,    "status": "Completed"},
        {"entryId": 201, "position": 2, "elapsedDurationMs": 573_500, "diffFirstMs": 1_500, "diffPrevMs": 1_500, "status": "Completed"},
        {"entryId": 205, "position": 3, "elapsedDurationMs": 575_200, "diffFirstMs": 3_200, "diffPrevMs": 1_700, "status": "Completed"},
        {"entryId": 202, "position": 4, "elapsedDurationMs": 577_400, "diffFirstMs": 5_400, "diffPrevMs": 2_200, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 579_800, "diffFirstMs": 7_800, "diffPrevMs": 2_400, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 583_100, "diffFirstMs": 11_100,"diffPrevMs": 3_300, "status": "Completed"},
    ],
    103: [  # SS3 — Lucéram (22.1 km) → ~17 min
        {"entryId": 201, "position": 1, "elapsedDurationMs": 1_018_000, "diffFirstMs": 0,      "diffPrevMs": 0,     "status": "Completed"},
        {"entryId": 203, "position": 2, "elapsedDurationMs": 1_020_500, "diffFirstMs": 2_500,  "diffPrevMs": 2_500, "status": "Completed"},
        {"entryId": 202, "position": 3, "elapsedDurationMs": 1_022_100, "diffFirstMs": 4_100,  "diffPrevMs": 1_600, "status": "Completed"},
        {"entryId": 205, "position": 4, "elapsedDurationMs": 1_025_300, "diffFirstMs": 7_300,  "diffPrevMs": 3_200, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 1_028_700, "diffFirstMs": 10_700, "diffPrevMs": 3_400, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 1_034_200, "diffFirstMs": 16_200, "diffPrevMs": 5_500, "status": "Completed"},
    ],
    104: [  # SS4 — Saint-Léger (15.8 km) → ~12 min
        {"entryId": 202, "position": 1, "elapsedDurationMs": 731_200, "diffFirstMs": 0,      "diffPrevMs": 0,     "status": "Completed"},
        {"entryId": 201, "position": 2, "elapsedDurationMs": 732_800, "diffFirstMs": 1_600,  "diffPrevMs": 1_600, "status": "Completed"},
        {"entryId": 205, "position": 3, "elapsedDurationMs": 734_500, "diffFirstMs": 3_300,  "diffPrevMs": 1_700, "status": "Completed"},
        {"entryId": 203, "position": 4, "elapsedDurationMs": 736_000, "diffFirstMs": 4_800,  "diffPrevMs": 1_500, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 739_400, "diffFirstMs": 8_200,  "diffPrevMs": 3_400, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 743_100, "diffFirstMs": 11_900, "diffPrevMs": 3_700, "status": "Completed"},
    ],
    105: [  # SS5 — Power Stage (18.55 km) → ~14 min
        {"entryId": 205, "position": 1, "elapsedDurationMs": 828_300, "diffFirstMs": 0,     "diffPrevMs": 0,    "status": "Completed"},
        {"entryId": 201, "position": 2, "elapsedDurationMs": 829_700, "diffFirstMs": 1_400, "diffPrevMs": 1_400, "status": "Completed"},
        {"entryId": 203, "position": 3, "elapsedDurationMs": 831_200, "diffFirstMs": 2_900, "diffPrevMs": 1_500, "status": "Completed"},
        {"entryId": 202, "position": 4, "elapsedDurationMs": 833_800, "diffFirstMs": 5_500, "diffPrevMs": 2_600, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 836_500, "diffFirstMs": 8_200, "diffPrevMs": 2_700, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 841_000, "diffFirstMs": 12_700,"diffPrevMs": 4_500, "status": "Completed"},
    ],
}

# ── Clasificación general acumulada ───────────────────────────────────────────
# Calculada acumulando los tiempos de etapa

MOCK_OVERALL: dict[int, list[dict]] = {
    101: [  # Tras SS1
        {"entryId": 201, "position": 1, "totalTimeMs": 834_500,   "diffFirstMs": 0,     "penaltyTimeMs": 0},
        {"entryId": 202, "position": 2, "totalTimeMs": 836_200,   "diffFirstMs": 1_700, "penaltyTimeMs": 0},
        {"entryId": 203, "position": 3, "totalTimeMs": 837_800,   "diffFirstMs": 3_300, "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 839_100,   "diffFirstMs": 4_600, "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 841_000,   "diffFirstMs": 6_500, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 844_300,   "diffFirstMs": 9_800, "penaltyTimeMs": 0},
    ],
    102: [  # Tras SS2
        {"entryId": 201, "position": 1, "totalTimeMs": 1_408_000, "diffFirstMs": 0,      "penaltyTimeMs": 0},
        {"entryId": 203, "position": 2, "totalTimeMs": 1_409_800, "diffFirstMs": 1_800,  "penaltyTimeMs": 0},
        {"entryId": 202, "position": 3, "totalTimeMs": 1_413_600, "diffFirstMs": 5_600,  "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 1_414_300, "diffFirstMs": 6_300,  "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 1_420_800, "diffFirstMs": 12_800, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 1_427_400, "diffFirstMs": 19_400, "penaltyTimeMs": 0},
    ],
    103: [  # Tras SS3
        {"entryId": 201, "position": 1, "totalTimeMs": 2_426_000, "diffFirstMs": 0,      "penaltyTimeMs": 0},
        {"entryId": 203, "position": 2, "totalTimeMs": 2_430_300, "diffFirstMs": 4_300,  "penaltyTimeMs": 0},
        {"entryId": 202, "position": 3, "totalTimeMs": 2_435_700, "diffFirstMs": 9_700,  "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 2_439_600, "diffFirstMs": 13_600, "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 2_449_500, "diffFirstMs": 23_500, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 2_461_600, "diffFirstMs": 35_600, "penaltyTimeMs": 0},
    ],
    104: [  # Tras SS4
        {"entryId": 201, "position": 1, "totalTimeMs": 3_158_800, "diffFirstMs": 0,      "penaltyTimeMs": 0},
        {"entryId": 203, "position": 2, "totalTimeMs": 3_166_300, "diffFirstMs": 7_500,  "penaltyTimeMs": 0},
        {"entryId": 202, "position": 3, "totalTimeMs": 3_166_900, "diffFirstMs": 8_100,  "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 3_174_100, "diffFirstMs": 15_300, "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 3_188_900, "diffFirstMs": 30_100, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 3_204_700, "diffFirstMs": 45_900, "penaltyTimeMs": 0},
    ],
    105: [  # Tras SS5 — Clasificación final
        {"entryId": 201, "position": 1, "totalTimeMs": 3_988_500, "diffFirstMs": 0,      "penaltyTimeMs": 0},
        {"entryId": 203, "position": 2, "totalTimeMs": 3_997_500, "diffFirstMs": 9_000,  "penaltyTimeMs": 0},
        {"entryId": 202, "position": 3, "totalTimeMs": 4_000_700, "diffFirstMs": 12_200, "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 4_002_400, "diffFirstMs": 13_900, "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 4_025_400, "diffFirstMs": 36_900, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 4_045_700, "diffFirstMs": 57_200, "penaltyTimeMs": 0},
    ],
}
