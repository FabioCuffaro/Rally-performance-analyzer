"""Página de comparativa — dos pilotos cara a cara."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components import api_client as api
from dashboard.components.charts import create_comparison_chart

st.set_page_config(page_title="Comparativa — Rally Analyzer", page_icon="🔀", layout="wide")

with st.sidebar:
    st.markdown("## 🏁 Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="🏠 Overview")
    st.page_link("pages/01_stages.py", label="⏱️ Etapas")
    st.page_link("pages/02_evolution.py", label="📈 Evolución")
    st.page_link("pages/03_compare.py", label="🔀 Comparativa")

st.title("🔀 Comparativa entre Pilotos")
st.divider()

# ── Carga de pilotos ──────────────────────────────────────────────────────────
drivers = api.get_drivers()
if not drivers:
    st.error("⚠️ No se puede conectar con la API.")
    st.stop()

driver_options = {
    f"{d['driver_name']} ({d['manufacturer']}) #{d['car_number']}": d
    for d in drivers
}
driver_names = list(driver_options.keys())

# ── Selectores ────────────────────────────────────────────────────────────────
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

# ── Comparativa ───────────────────────────────────────────────────────────────
result = api.compare_drivers(driver_a["entry_id"], driver_b["entry_id"])
if not result:
    st.error("No se pudo obtener la comparativa.")
    st.stop()

times_a = result.get("stage_times_a", [])
times_b = result.get("stage_times_b", [])

df_a = pd.DataFrame(times_a)
df_b = pd.DataFrame(times_b)

# ── KPIs de comparativa ───────────────────────────────────────────────────────
st.markdown(f"### {driver_a['driver_name']} vs {driver_b['driver_name']}")

if not df_a.empty and not df_b.empty:
    wins_a = sum(1 for _, ra in df_a.iterrows()
                 for _, rb in df_b.iterrows()
                 if ra["stage_code"] == rb["stage_code"] and
                 (ra.get("time_s") or 9999) < (rb.get("time_s") or 9999))
    wins_b = len(df_a) - wins_a

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(f"Etapas ganadas por {driver_a['driver_code']}", wins_a)
    with c2:
        st.metric(f"Etapas ganadas por {driver_b['driver_code']}", wins_b)
    with c3:
        st.metric("Total etapas", len(df_a))

st.divider()

# ── Gráfico comparativo ───────────────────────────────────────────────────────
fig = create_comparison_chart(
    df_a, df_b,
    driver_a["driver_name"], driver_b["driver_name"],
    driver_a.get("manufacturer", ""), driver_b.get("manufacturer", ""),
)
st.plotly_chart(fig, use_container_width=True)

# ── Tabla detallada ───────────────────────────────────────────────────────────
st.markdown("### 📋 Detalle por etapa")
if not df_a.empty and not df_b.empty:
    merged = df_a.merge(
        df_b, on="stage_code", suffixes=(f"_{driver_a['driver_code']}", f"_{driver_b['driver_code']}")
    )
    time_col_a = f"time_s_{driver_a['driver_code']}"
    time_col_b = f"time_s_{driver_b['driver_code']}"

    if time_col_a in merged.columns and time_col_b in merged.columns:
        merged["Diferencia (s)"] = (merged[time_col_a] - merged[time_col_b]).round(3)
        merged["Ganador"] = merged.apply(
            lambda r: driver_a["driver_code"] if r[time_col_a] < r[time_col_b]
            else driver_b["driver_code"], axis=1
        )
        display = merged[["stage_code", time_col_a, time_col_b, "Diferencia (s)", "Ganador"]].copy()
        display.columns = [
            "Etapa",
            f"Tiempo {driver_a['driver_code']} (s)",
            f"Tiempo {driver_b['driver_code']} (s)",
            "Diferencia (s)",
            "Ganador",
        ]
        st.dataframe(display, use_container_width=True, hide_index=True)
