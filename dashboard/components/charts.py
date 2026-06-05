"""
Graficos Plotly reutilizables para el dashboard.

Paleta profesional motorsport. Todas las funciones reciben un DataFrame
y devuelven un go.Figure listo para st.plotly_chart().
"""

from __future__ import annotations

import plotly.graph_objects as go
import pandas as pd

# ── Paleta coordinada con tema oscuro (config.toml base=dark) ─────────────────
# 20 colores visualmente distintos entre si, legibles sobre fondo oscuro.
# Se asignan por posicion de iteracion (no por fabricante) para que cada
# piloto tenga siempre un color unico aunque comparta equipo.
DRIVER_COLORS = [
    "#FF4B4B",  # rojo vivo
    "#4CC9F0",  # azul electrico
    "#F8961E",  # naranja
    "#7BF1A8",  # verde menta
    "#BB8FCE",  # lavanda
    "#FEE440",  # amarillo
    "#00F5D4",  # cyan
    "#9B5DE5",  # violeta
    "#F72585",  # rosa fuerte
    "#4361EE",  # azul indigo
    "#FB5607",  # naranja rojizo
    "#FFBE0B",  # ambar
    "#06D6A0",  # esmeralda
    "#EF233C",  # rojo carmesi
    "#8338EC",  # purpura
    "#3BF4FB",  # turquesa
    "#E9FF70",  # lima
    "#FF9F1C",  # mandarina
    "#2EC4B6",  # teal
    "#FF6FA8",  # rosa salmon
]

# Solo para la comparativa de dos pilotos donde el equipo aporta contexto visual
MANUFACTURER_COLORS: dict[str, str] = {
    "Toyota":  "#FF4B4B",
    "Hyundai": "#4CC9F0",
    "Ford":    "#F8961E",
    "Citroen": "#7BF1A8",
}

GRID_COLOR  = "#2D2D4E"
BG_COLOR    = "rgba(0,0,0,0)"   # transparente — hereda el fondo oscuro de Streamlit
FONT_COLOR  = "#FFFFFF"
FONT_FAMILY = "Inter, Arial, sans-serif"


def _driver_color(idx: int) -> str:
    return DRIVER_COLORS[idx % len(DRIVER_COLORS)]


def _manufacturer_color(manufacturer: str, idx: int = 0) -> str:
    return MANUFACTURER_COLORS.get(manufacturer, DRIVER_COLORS[idx % len(DRIVER_COLORS)])


def _base_layout(**kwargs) -> dict:
    """Layout base compartido por todos los graficos."""
    _axis = dict(
        gridcolor=GRID_COLOR,
        linecolor="#404060",
        tickfont=dict(color=FONT_COLOR),
        title_font=dict(color=FONT_COLOR),
    )
    base = dict(
        plot_bgcolor=BG_COLOR,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, size=12, color=FONT_COLOR),
        xaxis=_axis,
        yaxis=_axis,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=11, color=FONT_COLOR),
        ),
        margin=dict(l=10, r=90, t=55, b=45),
        hoverlabel=dict(bgcolor="#1A1A2E", font_size=12, font_color=FONT_COLOR),
    )
    base.update(kwargs)
    return base


# ── Grafico 1: Tiempos de etapa (bar horizontal) ──────────────────────────────

def create_stage_times_chart(df: pd.DataFrame, stage_code: str) -> go.Figure:
    """
    Bar chart horizontal de tiempos por etapa.
    Eje Y: nombre del piloto + fabricante. Eje X: tiempo en segundos.
    """
    if df.empty:
        return go.Figure()

    df = df.sort_values("position", ascending=False).copy()

    df["y_label"] = df.apply(
        lambda r: f"{r.get('driver_name','?')}  #{r.get('car_number','')}", axis=1
    )
    df["gap_label"] = df["diff_first_s"].apply(
        lambda x: "LIDER" if (x == 0 or pd.isna(x)) else f"+{x:.3f}s"
    )

    # Color unico por piloto segun su posicion en el ranking
    colors = [_driver_color(i) for i in range(len(df))]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["time_s"],
        y=df["y_label"],
        orientation="h",
        marker=dict(color=colors, opacity=0.85),
        text=df["gap_label"],
        textposition="outside",
        textfont=dict(size=11, color=FONT_COLOR),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Tiempo: %{x:.3f}s<br>"
            "Gap lider: %{text}<extra></extra>"
        ),
    ))

    x_min = df["time_s"].min()
    x_max = df["time_s"].max()
    margin = (x_max - x_min) * 0.15

    layout = _base_layout(
        title=dict(text=f"Tiempos de etapa — {stage_code}", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(
            title="Tiempo (s)",
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
            range=[x_min * 0.998, x_max + margin],
        ),
        yaxis=dict(
            title="",
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            automargin=True,
        ),
        height=350,
        margin=dict(l=10, r=100, t=50, b=45),
    )
    fig.update_layout(**layout)
    return fig


# ── Grafico 2: Gap acumulado respecto al lider ────────────────────────────────

def create_gap_evolution_chart(df: pd.DataFrame) -> go.Figure:
    """
    Line chart del gap acumulado respecto al lider etapa a etapa.
    Eje X: etapas. Eje Y: segundos de diferencia.
    """
    if df.empty:
        return go.Figure()

    stage_order = df.drop_duplicates("stage_id").sort_values("stage_id")["stage_code"].tolist()

    fig = go.Figure()
    drivers = df.drop_duplicates("entry_id").sort_values("entry_id")

    for idx, (_, row) in enumerate(drivers.iterrows()):
        entry_id = row["entry_id"]
        code = row.get("driver_code", str(entry_id))
        color = _driver_color(idx)

        d = df[df["entry_id"] == entry_id].copy()
        d["stage_code"] = pd.Categorical(d["stage_code"], categories=stage_order, ordered=True)
        d = d.sort_values("stage_code")

        fig.add_trace(go.Scatter(
            x=d["stage_code"].astype(str),
            y=d["diff_first_s"].fillna(0),
            mode="lines+markers",
            name=code,
            line=dict(color=color, width=2.5),
            marker=dict(size=8, color=color, line=dict(width=1.5, color="white")),
            hovertemplate=(
                f"<b>{code}</b><br>"
                "Etapa: %{x}<br>"
                "Gap lider: +%{y:.1f}s<extra></extra>"
            ),
        ))

    layout = _base_layout(
        title=dict(text="Gap acumulado respecto al lider", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=stage_order,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=12, color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        yaxis=dict(
            title="Diferencia (s)",
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
            rangemode="tozero",
        ),
        height=400,
    )
    fig.update_layout(**layout)
    return fig


# ── Grafico 3: Evolucion de posiciones (bump chart) ───────────────────────────

def create_position_evolution_chart(df: pd.DataFrame) -> go.Figure:
    """
    Bump chart: posicion de cada piloto en cada etapa.
    Eje Y invertido (posicion 1 arriba). Eje X: etapas categoricas.
    """
    if df.empty:
        return go.Figure()

    stage_order = df.drop_duplicates("stage_id").sort_values("stage_id")["stage_code"].tolist()
    n_drivers = df["entry_id"].nunique()

    fig = go.Figure()
    drivers = df.drop_duplicates("entry_id").sort_values("entry_id")

    for idx, (_, row) in enumerate(drivers.iterrows()):
        entry_id = row["entry_id"]
        code = row.get("driver_code", str(entry_id))
        name = row.get("driver_name", code)
        color = _driver_color(idx)

        d = df[df["entry_id"] == entry_id].copy()
        d["stage_code"] = pd.Categorical(d["stage_code"], categories=stage_order, ordered=True)
        d = d.sort_values("stage_code")

        fig.add_trace(go.Scatter(
            x=d["stage_code"].astype(str),
            y=d["position"],
            mode="lines+markers",
            name=code,
            line=dict(color=color, width=3),
            marker=dict(
                size=12, color=color,
                line=dict(width=2, color="white"),
                symbol="circle",
            ),
            hovertemplate=(
                f"<b>{name}</b><br>"
                "Etapa: %{x}<br>"
                "Posicion: %{y}<extra></extra>"
            ),
        ))

    layout = _base_layout(
        title=dict(text="Evolucion de posiciones por etapa", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=stage_order,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=13, color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        yaxis=dict(
            title="Posicion",
            autorange="reversed",
            tickmode="linear",
            tick0=1,
            dtick=1,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=12, color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
            range=[n_drivers + 0.5, 0.5],
        ),
        height=440,
        margin=dict(l=10, r=10, t=55, b=45),
    )
    fig.update_layout(**layout)
    return fig


# ── Grafico 4: Comparativa entre dos pilotos ─────────────────────────────────

def create_comparison_chart(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    name_a: str,
    name_b: str,
    manufacturer_a: str = "",
    manufacturer_b: str = "",
) -> go.Figure:
    """
    Grouped bar chart: tiempos de etapa de dos pilotos lado a lado.
    Aqui si se usan colores de fabricante porque el contexto visual aporta informacion.
    """
    if df_a.empty or df_b.empty:
        return go.Figure()

    color_a = _manufacturer_color(manufacturer_a, 0)
    color_b = _manufacturer_color(manufacturer_b, 1)

    stage_order = df_a.sort_values("stage_id")["stage_code"].tolist() if "stage_id" in df_a.columns \
        else df_a["stage_code"].tolist()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=name_a,
        x=df_a.sort_values("stage_id")["stage_code"] if "stage_id" in df_a.columns else df_a["stage_code"],
        y=df_a.sort_values("stage_id")["time_s"] if "stage_id" in df_a.columns else df_a["time_s"],
        marker=dict(color=color_a, opacity=0.85),
        hovertemplate=f"<b>{name_a}</b><br>Etapa: %{{x}}<br>Tiempo: %{{y:.3f}}s<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name=name_b,
        x=df_b.sort_values("stage_id")["stage_code"] if "stage_id" in df_b.columns else df_b["stage_code"],
        y=df_b.sort_values("stage_id")["time_s"] if "stage_id" in df_b.columns else df_b["time_s"],
        marker=dict(color=color_b, opacity=0.85),
        hovertemplate=f"<b>{name_b}</b><br>Etapa: %{{x}}<br>Tiempo: %{{y:.3f}}s<extra></extra>",
    ))

    layout = _base_layout(
        title=dict(text=f"Comparativa: {name_a} vs {name_b}", font=dict(size=15, color=FONT_COLOR)),
        barmode="group",
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=stage_order,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=13, color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        yaxis=dict(
            title="Tiempo (s)",
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        height=380,
    )
    fig.update_layout(**layout)
    return fig
