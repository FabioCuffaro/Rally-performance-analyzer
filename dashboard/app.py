from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import streamlit as st
from dashboard.components import api_client as api

st.set_page_config(page_title="Rally Performance Analyzer", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.markdown("## Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="Overview")
    st.page_link("pages/01_stages.py", label="Etapas")
    st.page_link("pages/02_evolution.py", label="Evolucion")
    st.page_link("pages/03_compare.py", label="Comparativa")
    st.markdown("---")
    st.caption("Datos: Rally Monte Carlo 2024")

st.title("Rally Performance Analyzer")
st.markdown("**World Rally Championship - Analisis de datos**")
st.divider()

rallies = api.get_rallies()
classification = api.get_classification()
stages = api.get_stages()
drivers = api.get_drivers()

if not rallies or not classification:
    st.error("No se puede conectar con la API. Arranca FastAPI primero.")
    st.code("uvicorn backend.app.main:app --reload")
    st.stop()

rally = rallies[0]
entries = classification.get("entries", [])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Rally", rally["name"].replace("Rallye Automobile ", ""))
with col2:
    st.metric("Pais", rally["country"])
with col3:
    st.metric("Etapas", len(stages))
with col4:
    st.metric("Pilotos", len(drivers))

st.divider()
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### Clasificacion General Final")
    if entries:
        rows = []
        for e in entries:
            gap = e.get("diff_first_s", 0) or 0
            gap_str = "LIDER" if gap == 0 else f"+{gap:.1f}s"
            rows.append({"Pos.": e["position"], "Piloto": e["driver_name"], "#": e.get("car_number", ""), "Fabricante": e.get("manufacturer", ""), "Tiempo total": e.get("total_time_str", "-"), "Gap": gap_str})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with col_right:
    st.markdown("### Fabricantes")
    fab_data = {}
    for e in entries:
        fab = e.get("manufacturer", "Otro")
        fab_data[fab] = fab_data.get(fab, 0) + 1
    for fab, count in sorted(fab_data.items()):
        st.markdown(f"**{fab}** - {count} pilotos")
    st.markdown("---")
    st.markdown("### Podio")
    medals = ["1.", "2.", "3."]
    for e in entries[:3]:
        gap = e.get("diff_first_s", 0) or 0
        gap_str = "LIDER" if gap == 0 else f"+{gap:.1f}s"
        st.markdown(f"{medals[e['position']-1]} **{e['driver_name']}** ({e.get('manufacturer','')}) - {gap_str}")
