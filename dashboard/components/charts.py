"""
Graficos Plotly reutilizables para el dashboard.

Paleta profesional motorsport. Todas las funciones reciben un DataFrame
y devuelven un go.Figure listo para st.plotly_chart().
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Paleta de colores profesional ─────────────────────────────────────────────
MANUFACTURER_COLORS: dict[str, str] = {
    "Toyota":  "#C8102E",   # rojo Toyota (mas sobrio que el original)
    "Hyundai": "#003B8E",   # azul marino Hyundai
    "Ford":    "#003399",
    "Citroen": "#C60C30",
}

# Paleta suave para pilotos sin fabricante conocido
FALLBACK_COLORS = [
    "#E63946", "#457B9D", "#2A9D8F", "#E9C46A",
    "#F4A261", "#264653", "#6A4C93", "#1982C4",
]

GRID_COLOR   = "#E8E8E8"
BG_COLOR     = "#FAFAFA"
FONT_COLOR   = "#1A1A2E"
FONT_FAMILY  = "Inter, Arial, sans-serif"


def _color(manufacturer: str, idx: int = 0) -> str:
    return MANUFACTURER_COLORS.get(manufacturer, FALLBACK_COLORS[idx % len(FALLBACK_COLORS)])


def _base_layout(**kwargs) -> dict:
    """Layout base compartido por todos los graficos."""
    base = dict(
        plot_bgcolor="rgba(0,0,0,0)",
paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, size=12, color="#FFFFFF"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.15)", linecolor="rgba(255,255,255,0.3)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.15)", linecolor="rgba(255,255,255,0.3)"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=11),
        ),
        margin=dict(l=10, r=90, t=55, b=45),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    base.update(kwargs)
    return base


# ── Grafico 1: Tiempos de etapa (bar horizontal) ──────────────────────────────

def create_stage_times_chart(df: pd.DataFrame, stage_code: str) -> go.Figure:
    """
    Bar chart horizontal de tiempos por etapa.
    Eje Y: nombre del piloto + numero de coche. Eje X: tiempo en segundos.
    """
    if df.empty:
        return go.Figure()

    df = df.sort_values("position", ascending=False).reset_index(drop=True)

    # Construccion vectorizada de etiquetas (evita r.get() que puede devolver NaN)
    df["y_label"] = (
        df["driver_name"].fillna("?").astype(str)
        + "  #"
        + df["car_number"].fillna("").astype(str)
    )
    df["gap_label"] = df["diff_first_s"].apply(
        lambda x: "LIDER" if (pd.isna(x) or x == 0) else f"+{x:.3f}s"
    )

    y_vals  = df["y_label"].tolist()
    x_vals  = df["time_s"].tolist()
    colors  = [_color(m, i) for i, m in enumerate(df["manufacturer"].fillna("").tolist())]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_vals,
        y=y_vals,
        orientation="h",
        marker=dict(color=colors, opacity=0.85),
        text=df["gap_label"].tolist(),
        textposition="outside",
        textfont=dict(size=11, color=FONT_COLOR),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Tiempo: %{x:.3f}s<br>"
            "Gap lider: %{text}<extra></extra>"
        ),
    ))

    x_min = min(x_vals)
    x_max = max(x_vals)
    x_range_margin = (x_max - x_min) * 0.15

    fig.update_layout(**_base_layout(
        title=dict(text=f"Tiempos de etapa — {stage_code}", font=dict(size=15)),
        xaxis=dict(
            title="Tiempo (s)",
            gridcolor=GRID_COLOR,
            range=[x_min * 0.998, x_max + x_range_margin],
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            # tickvals/ticktext fuerzan a Plotly a mostrar los nombres en el eje Y
            tickmode="array",
            tickvals=y_vals,
            ticktext=y_vals,
            automargin=True,
        ),
        height=max(300, len(df) * 38 + 80),
        margin=dict(l=180, r=110, t=55, b=45),
    ))
    return fig


# ── Grafico 2: Gap acumulado respecto al lider ────────────────────────────────

def create_gap_evolution_chart(df: pd.DataFrame) -> go.Figure:
    """
    Line chart del gap acumulado respecto al lider etapa a etapa.
    Eje X: etapas. Eje Y: segundos de diferencia.
    """
    if df.empty:
        return go.Figure()

    # Ordenar etapas cronologicamente
    stage_order = df.drop_duplicates("stage_id").sort_values("stage_id")["stage_code"].tolist()

    fig = go.Figure()
    drivers = df.drop_duplicates("entry_id").sort_values("entry_id")

    for i, row in drivers.iterrows():
        entry_id = row["entry_id"]
        code = row.get("driver_code", str(entry_id))
        manufacturer = row.get("manufacturer", "")
        color = _color(manufacturer, i)

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
        title=dict(text="Gap acumulado respecto al lider", font=dict(size=15)),
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=stage_order,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            title="Diferencia (s)",
            gridcolor=GRID_COLOR,
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

    for i, row in drivers.iterrows():
        entry_id = row["entry_id"]
        code = row.get("driver_code", str(entry_id))
        name = row.get("driver_name", code)
        manufacturer = row.get("manufacturer", "")
        color = _color(manufacturer, i)

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
        title=dict(text="Evolucion de posiciones por etapa", font=dict(size=15)),
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=stage_order,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=13),
        ),
        yaxis=dict(
            title="Posicion",
            autorange="reversed",
            tickmode="linear",
            tick0=1,
            dtick=1,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=12),
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
    """
    if df_a.empty or df_b.empty:
        return go.Figure()

    color_a = _color(manufacturer_a, 0)
    color_b = _color(manufacturer_b, 1)

    # Ordenar ambos DFs y convertir a listas Python para evitar problemas
    # de alineacion por indice de pandas con go.Bar
    sort_col = "stage_id" if "stage_id" in df_a.columns else "stage_code"
    df_a = df_a.sort_values(sort_col).reset_index(drop=True)
    df_b = df_b.sort_values(sort_col).reset_index(drop=True)

    stages_a  = df_a["stage_code"].tolist()
    stages_b  = df_b["stage_code"].tolist()
    all_stages = sorted(set(stages_a) | set(stages_b))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=name_a,
        x=stages_a,
        y=df_a["time_s"].tolist(),
        marker=dict(color=color_a, opacity=0.85),
        hovertemplate=f"<b>{name_a}</b><br>Etapa: %{{x}}<br>Tiempo: %{{y:.3f}}s<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name=name_b,
        x=stages_b,
        y=df_b["time_s"].tolist(),
        marker=dict(color=color_b, opacity=0.85),
        hovertemplate=f"<b>{name_b}</b><br>Etapa: %{{x}}<br>Tiempo: %{{y:.3f}}s<extra></extra>",
    ))

    fig.update_layout(**_base_layout(
        title=dict(text=f"Comparativa: {name_a} vs {name_b}", font=dict(size=15)),
        barmode="group",
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=all_stages,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=13),
        ),
        yaxis=dict(title="Tiempo (s)", gridcolor=GRID_COLOR),
        height=380,
    ))
    return fig
