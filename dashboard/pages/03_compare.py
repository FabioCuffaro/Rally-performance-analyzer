"""Pagina de comparativa — dos pilotos cara a cara."""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import streamlit as st

from dashboard.components import api_client as api
from dashboard.components.charts import create_comparison_chart

st.set_page_config(page_title="Comparativa — Rally Analyzer", page_icon="🔀", layout="wide")

with st.sidebar:
    st.markdown("## Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="Overview")
    st.page_link("pages/01_stages.py", label="Etapas")
    st.page_link("pages/02_evolution.py", label="Evolucion")
    st.page_link("pages/03_compare.py", label="Comparativa")

st.title("Comparativa entre Pilotos")
st.divider()

drivers = api.get_drivers()
if not drivers:
    st.error("No se puede conectar con la API.")
    st.stop()

driver_options = {
    f"{d['driver_name']} ({d['manufacturer']}) #{d['car_number']}": d
    for d in drivers
}
driver_names = list(driver_options.keys())

col1, col2 = st.columns(2)
with col1:
    sel_a = st.selectbox("Piloto A", driver_names, index=0)
with col2:
    sel_b = st.selectbox("Piloto B", driver_names, index=1)

driver_a = driver_options[sel_a]
driver_b = driver_options[sel_b]

if driver_a["entry_id"] == driver_b["entry_id"]:
    st.warning("Selecciona dos pilotos diferentes.")
    st.stop()

result = api.compare_drivers(driver_a["entry_id"], driver_b["entry_id"])
if not result:
    st.error("No se pudo obtener la comparativa.")
    st.stop()

times_a = result.get("stage_times_a", [])
times_b = result.get("stage_times_b", [])

df_a = pd.DataFrame(times_a)
df_b = pd.DataFrame(times_b)

if df_a.empty or df_b.empty:
    st.warning("No hay datos de tiempos disponibles.")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown(f"### {driver_a['driver_name']} vs {driver_b['driver_name']}")

# Calcular victorias por etapa correctamente (un registro por etapa)
df_a_sorted = df_a.sort_values("stage_code").reset_index(drop=True)
df_b_sorted = df_b.sort_values("stage_code").reset_index(drop=True)

wins_a = 0
wins_b = 0
for _, ra in df_a_sorted.iterrows():
    match = df_b_sorted[df_b_sorted["stage_code"] == ra["stage_code"]]
    if not match.empty:
        ta = ra.get("time_s") or 9999
        tb = match.iloc[0].get("time_s") or 9999
        if ta < tb:
            wins_a += 1
        else:
            wins_b += 1

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(f"Etapas ganadas — {driver_a['driver_code']}", wins_a)
with c2:
    st.metric(f"Etapas ganadas — {driver_b['driver_code']}", wins_b)
with c3:
    st.metric("Total etapas", len(df_a_sorted))

st.divider()

# ── Grafico ───────────────────────────────────────────────────────────────────
fig = create_comparison_chart(
    df_a_sorted, df_b_sorted,
    driver_a["driver_name"], driver_b["driver_name"],
    driver_a.get("manufacturer", ""), driver_b.get("manufacturer", ""),
)
st.plotly_chart(fig, use_container_width=True)

# ── Tabla detallada (sin duplicados) ──────────────────────────────────────────
st.markdown("### Detalle por etapa")

rows = []
for _, ra in df_a_sorted.iterrows():
    stage = ra["stage_code"]
    match = df_b_sorted[df_b_sorted["stage_code"] == stage]
    if match.empty:
        continue
    rb = match.iloc[0]
    ta = ra.get("time_s") or 0
    tb = rb.get("time_s") or 0
    diff = round(ta - tb, 3)
    winner = driver_a["driver_code"] if ta < tb else driver_b["driver_code"]
    rows.append({
        "Etapa": stage,
        f"Tiempo {driver_a['driver_code']} (s)": ta,
        f"Tiempo {driver_b['driver_code']} (s)": tb,
        "Diferencia (s)": diff,
        "Ganador": winner,
    })

df_table = pd.DataFrame(rows)
st.dataframe(df_table, use_container_width=True, hide_index=True)
