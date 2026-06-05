"""Pagina de etapas — tiempos por etapa con selector."""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import streamlit as st

from dashboard.components import api_client as api
from dashboard.components.charts import create_stage_times_chart

st.set_page_config(page_title="Etapas — Rally Analyzer", page_icon="⏱️", layout="wide")

with st.sidebar:
    st.markdown("## Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="Overview")
    st.page_link("pages/01_stages.py", label="Etapas")
    st.page_link("pages/02_evolution.py", label="Evolucion")
    st.page_link("pages/03_compare.py", label="Comparativa")

st.title("Tiempos por Etapa")
st.divider()

stages = api.get_stages()
if not stages:
    st.error("No se puede conectar con la API.")
    st.stop()

stage_options = {f"{s['stage_code']} — {s['name']} ({s['distance_km']} km)": s for s in stages}
selected_label = st.selectbox("Selecciona una etapa", list(stage_options.keys()))
selected_stage = stage_options[selected_label]
stage_id   = selected_stage["stage_id"]
stage_code = selected_stage["stage_code"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Codigo", stage_code)
with col2:
    st.metric("Distancia", f"{selected_stage['distance_km']} km")
with col3:
    st.metric("Superficie", selected_stage.get("surface", "-"))

st.divider()

result = api.get_stage_times(stage_id)
if not result or not result.get("entries"):
    st.warning("No hay tiempos disponibles para esta etapa.")
    st.stop()

entries = result["entries"]
df = pd.DataFrame(entries)

fig = create_stage_times_chart(df, stage_code)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Tabla de tiempos")
table_rows = []
for e in entries:
    gap  = e.get("diff_first_s", 0) or 0
    prev = e.get("diff_prev_s", 0) or 0
    table_rows.append({
        "Pos.":        e["position"],
        "Piloto":      e["driver_name"],
        "#":           e.get("car_number", ""),
        "Fabricante":  e.get("manufacturer", ""),
        "Tiempo":      e.get("time_str", "-"),
        "Gap lider":   "LIDER" if gap == 0 else f"+{gap:.3f}s",
        "Gap anterior": "—" if prev == 0 else f"+{prev:.3f}s",
    })

st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
