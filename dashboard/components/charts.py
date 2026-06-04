"""
Componentes de gráficos reutilizables — Plotly.

Cada función recibe datos ya procesados y devuelve una figura Plotly.
"""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ── Paleta de colores ─────────────────────────────────────────────────────────
MANUFACTURER_COLORS = {
    "Toyota":  "#EB0A1E",
    "Hyundai": "#003399",
    "Ford":    "#003876",
    "Citroën": "#E3002B",
}

DEFAULT_COLORS = px.colors.qualitative.Set2


def _driver_color(manufacturer: str, idx: int = 0) -> str:
    return MANUFACTURER_COLORS.get(manufacturer, DEFAULT_COLORS[idx % len(DEFAULT_COLORS)])


# ── Gráfico 1: Tiempos de etapa (bar chart horizontal) ───────────────────────

def create_stage_times_chart(df: pd.DataFrame, stage_code: str) -> go.Figure:
    """
    Bar chart horizontal con los tiempos de una etapa.
    Barras coloreadas por fabricante, con gap vs líder anotado.
    """
    if df.empty:
        return go.Figure()

    df = df.sort_values("position", ascending=False).copy()
    df["label"] = df["driver_code"] + " (#" + df["car_number"].astype(str) + ")"
    df["gap_str"] = df["diff_first_s"].apply(
        lambda x: "LÍDER" if x == 0 else f"+{x:.1f}s"
    )
    colors = [_driver_color(m, i) for i, m in enumerate(df["manufacturer"])]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["time_s"],
        y=df["label"],
        orientation="h",
        marker_color=colors,
        text=df["gap_str"],
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Tiempo: %{x:.3f}s<br>"
            "Gap líder: %{text}<extra></extra>"
        ),
    ))

    fig.update_layout(
        title=f"Tiempos — {stage_code}",
        xaxis_title="Tiempo (s)",
        yaxis_title="",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        margin=dict(l=10, r=80, t=50, b=40),
        height=320,
        xaxis=dict(
            gridcolor="#eeeeee",
            range=[df["time_s"].min() * 0.995, df["time_s"].max() * 1.01],
        ),
    )
    return fig


# ── Gráfico 2: Gap acumulado respecto al líder ────────────────────────────────

def create_gap_evolution_chart(df: pd.DataFrame) -> go.Figure:
    """
    Line chart del gap acumulado respecto al líder a lo largo del rally.
    Una línea por piloto (excluye al líder que siempre es 0).
    """
    if df.empty:
        return go.Figure()

    fig = go.Figure()
    drivers = df["driver_code"].unique()

    for i, code in enumerate(drivers):
        d = df[df["driver_code"] == code].sort_values("stage_id")
        manufacturer = d["manufacturer"].iloc[0] if "manufacturer" in d.columns else ""
        color = _driver_color(manufacturer, i)

        fig.add_trace(go.Scatter(
            x=d["stage_code"],
            y=d["diff_first_s"],
            mode="lines+markers",
            name=code,
            line=dict(color=color, width=2),
            marker=dict(size=7),
            hovertemplate=(
                f"<b>{code}</b><br>"
                "Etapa: %{x}<br>"
                "Gap líder: +%{y:.1f}s<extra></extra>"
            ),
        ))

    fig.update_layout(
        title="Gap acumulado respecto al líder",
        xaxis_title="Etapa",
        yaxis_title="Segundos (+s)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=60, b=40),
        height=380,
        xaxis=dict(gridcolor="#eeeeee"),
        yaxis=dict(gridcolor="#eeeeee"),
    )
    return fig


# ── Gráfico 3: Evolución de posiciones (bump chart) ───────────────────────────

def create_position_evolution_chart(df: pd.DataFrame) -> go.Figure:
    """
    Bump chart: evolución de la posición de cada piloto etapa a etapa.
    Eje Y invertido (posición 1 arriba).
    """
    if df.empty:
        return go.Figure()

    fig = go.Figure()
    drivers = df["driver_code"].unique()

    for i, code in enumerate(drivers):
        d = df[df["driver_code"] == code].sort_values("stage_id")
        manufacturer = d["manufacturer"].iloc[0] if "manufacturer" in d.columns else ""
        color = _driver_color(manufacturer, i)

        fig.add_trace(go.Scatter(
            x=d["stage_code"],
            y=d["position"],
            mode="lines+markers+text",
            name=code,
            line=dict(color=color, width=2.5),
            marker=dict(size=10, color=color),
            text=d["position"],
            textposition="middle right",
            textfont=dict(size=10, color=color),
            hovertemplate=(
                f"<b>{code}</b><br>"
                "Etapa: %{x}<br>"
                "Posición: %{y}<extra></extra>"
            ),
        ))

    n_stages = df["stage_id"].nunique()
    fig.update_layout(
        title="Evolución de posiciones",
        xaxis_title="Etapa",
        yaxis_title="Posición",
        yaxis=dict(
            autorange="reversed",
            tickmode="linear",
            tick0=1,
            dtick=1,
            gridcolor="#eeeeee",
        ),
        xaxis=dict(gridcolor="#eeeeee"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=60, t=60, b=40),
        height=420,
    )
    return fig


# ── Gráfico 4: Comparativa entre dos pilotos ─────────────────────────────────

def create_comparison_chart(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    name_a: str,
    name_b: str,
    manufacturer_a: str = "",
    manufacturer_b: str = "",
) -> go.Figure:
    """
    Grouped bar chart comparando los tiempos de etapa de dos pilotos.
    """
    if df_a.empty or df_b.empty:
        return go.Figure()

    color_a = _driver_color(manufacturer_a, 0)
    color_b = _driver_color(manufacturer_b, 1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=name_a,
        x=df_a["stage_code"],
        y=df_a["time_s"],
        marker_color=color_a,
        hovertemplate=f"<b>{name_a}</b><br>Etapa: %{{x}}<br>Tiempo: %{{y:.3f}}s<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name=name_b,
        x=df_b["stage_code"],
        y=df_b["time_s"],
        marker_color=color_b,
        hovertemplate=f"<b>{name_b}</b><br>Etapa: %{{x}}<br>Tiempo: %{{y:.3f}}s<extra></extra>",
    ))

    fig.update_layout(
        title=f"Comparativa: {name_a} vs {name_b}",
        barmode="group",
        xaxis_title="Etapa",
        yaxis_title="Tiempo (s)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=60, b=40),
        height=360,
        xaxis=dict(gridcolor="#eeeeee"),
        yaxis=dict(gridcolor="#eeeeee"),
    )
    return fig
