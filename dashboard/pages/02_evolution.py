"""Pagina de evolucion — bump chart y gap acumulado."""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import streamlit as st

from dashboard.components import api_client as api
from dashboard.components.charts import (
    create_gap_evolution_chart,
    create_position_evolution_chart,
)

st.set_page_config(page_title="Evolucion — Rally Analyzer", page_icon="📈", layout="wide")

with st.sidebar:
    st.markdown("## Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="Overview")
    st.page_link("pages/01_stages.py", label="Etapas")
    st.page_link("pages/02_evolution.py", label="Evolucion")
    st.page_link("pages/03_compare.py", label="Comparativa")

st.title("Evolucion del Rally")
st.divider()

evolution = api.get_evolution()
if not evolution:
    st.error("No se puede conectar con la API.")
    st.stop()

# Construir DataFrame plano
rows = []
for driver in evolution:
    for pos in driver["positions"]:
        rows.append({
            "entry_id":    driver["entry_id"],
            "driver_name": driver["driver_name"],
            "driver_code": driver["driver_code"],
            "manufacturer": driver["manufacturer"],
            "stage_id":    pos["stage_id"],
            "stage_code":  pos["stage_code"],
            "position":    pos["position"],
            "diff_first_s": pos.get("diff_first_s") or 0,
        })

df = pd.DataFrame(rows)

if df.empty or df["stage_code"].str.strip().eq("").all():
    st.warning("No hay datos de evolucion disponibles. Verifica que el pipeline se ejecuto correctamente.")
    st.stop()

# Filtro de pilotos
all_drivers = sorted(df["driver_code"].unique())
selected = st.multiselect("Filtrar pilotos (vacio = todos)", options=all_drivers, default=[])
df_filtered = df[df["driver_code"].isin(selected)] if selected else df

# Bump chart
st.markdown("### Posicion a lo largo del rally")
fig_bump = create_position_evolution_chart(df_filtered)
st.plotly_chart(fig_bump, use_container_width=True)

# Gap chart (excluir lider)
st.markdown("### Gap acumulado respecto al lider")
df_gap = df_filtered[df_filtered["diff_first_s"] > 0].copy()
if df_gap.empty:
    st.info("El lider no tiene gap. Selecciona otros pilotos para ver diferencias.")
else:
    fig_gap = create_gap_evolution_chart(df_gap)
    st.plotly_chart(fig_gap, use_container_width=True)

# Tabla pivot
st.markdown("### Posiciones por etapa")
try:
    stage_order = df_filtered.drop_duplicates("stage_id").sort_values("stage_id")["stage_code"].tolist()
    pivot = df_filtered.pivot_table(
        index=["driver_code", "manufacturer"],
        columns="stage_code",
        values="position",
        aggfunc="first",
    ).reset_index()
    pivot.columns.name = None
    # Reordenar columnas por etapa
    fixed_cols = ["driver_code", "manufacturer"]
    stage_cols = [c for c in stage_order if c in pivot.columns]
    pivot = pivot[fixed_cols + stage_cols]
    st.dataframe(pivot, use_container_width=True, hide_index=True)
except Exception:
    pass
