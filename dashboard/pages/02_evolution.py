"""Página de evolución — bump chart y gap acumulado."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components import api_client as api
from dashboard.components.charts import (
    create_gap_evolution_chart,
    create_position_evolution_chart,
)

st.set_page_config(page_title="Evolución — Rally Analyzer", page_icon="📈", layout="wide")

with st.sidebar:
    st.markdown("## 🏁 Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="🏠 Overview")
    st.page_link("pages/01_stages.py", label="⏱️ Etapas")
    st.page_link("pages/02_evolution.py", label="📈 Evolución")
    st.page_link("pages/03_compare.py", label="🔀 Comparativa")

st.title("📈 Evolución del Rally")
st.divider()

# ── Carga de datos ────────────────────────────────────────────────────────────
evolution = api.get_evolution()
if not evolution:
    st.error("⚠️ No se puede conectar con la API.")
    st.stop()

# Construir DataFrame plano
rows = []
for driver in evolution:
    for pos in driver["positions"]:
        rows.append({
            "entry_id": driver["entry_id"],
            "driver_name": driver["driver_name"],
            "driver_code": driver["driver_code"],
            "manufacturer": driver["manufacturer"],
            "stage_id": pos["stage_id"],
            "stage_code": pos["stage_code"],
            "position": pos["position"],
            "diff_first_s": pos.get("diff_first_s", 0) or 0,
        })

df = pd.DataFrame(rows)

# ── Filtro de pilotos ─────────────────────────────────────────────────────────
all_drivers = sorted(df["driver_code"].unique())
selected = st.multiselect(
    "Filtrar pilotos (vacío = todos)",
    options=all_drivers,
    default=[],
)
if selected:
    df_filtered = df[df["driver_code"].isin(selected)]
else:
    df_filtered = df

# ── Gráfico 1: Bump chart ─────────────────────────────────────────────────────
st.markdown("### 🎯 Posición a lo largo del rally")
fig_bump = create_position_evolution_chart(df_filtered)
st.plotly_chart(fig_bump, use_container_width=True)

# ── Gráfico 2: Gap acumulado ──────────────────────────────────────────────────
st.markdown("### ⏳ Gap acumulado respecto al líder")

# Excluir al líder en cada etapa (diff=0 constante no aporta info)
df_gap = df_filtered[df_filtered["diff_first_s"] > 0].copy()
if df_gap.empty:
    st.info("Solo hay un piloto seleccionado — el líder no tiene gap.")
else:
    fig_gap = create_gap_evolution_chart(df_gap)
    st.plotly_chart(fig_gap, use_container_width=True)

# ── Tabla resumen ─────────────────────────────────────────────────────────────
st.markdown("### 📋 Posiciones por etapa")
pivot = df_filtered.pivot_table(
    index=["driver_code", "manufacturer"],
    columns="stage_code",
    values="position",
    aggfunc="first",
).reset_index()
pivot.columns.name = None
st.dataframe(pivot, use_container_width=True, hide_index=True)
