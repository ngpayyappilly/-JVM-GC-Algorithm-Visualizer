import streamlit as st
import plotly.graph_objects as go
from algorithms import G1_LAYOUTS, REGION_TYPE_CFG
from styles import PLOTLY_BASE, hex_to_rgba


def render_heap(algo, phase, young_pct, old_pct, is_stw):
    if algo["heap_model"] == "regions":
        _render_g1_grid(phase, is_stw)
        _render_region_legend()
    else:
        _render_heap_bars(algo, young_pct, old_pct, is_stw)


def _render_region_legend():
    items = []
    for rtype in (0, 1, 2, 3, 4, 5, 6):
        cfg = REGION_TYPE_CFG[rtype]
        items.append(
            f'<div class="region-legend-item">'
            f'<div class="region-legend-swatch" style="background:{cfg["fill"]};border-color:{cfg["border"]}"></div>'
            f'{cfg["label"]} {cfg["name"]}</div>'
        )
    st.markdown(f'<div class="region-legend">{"".join(items)}</div>', unsafe_allow_html=True)


def _render_g1_grid(phase, is_stw):
    layout = G1_LAYOUTS.get(phase["id"], G1_LAYOUTS["alloc"])
    fig = go.Figure()
    fig.update_layout(
        **PLOTLY_BASE,
        width=480, height=280,
        xaxis=dict(visible=False, range=[0, 5]),
        yaxis=dict(visible=False, range=[0, 4], scaleanchor="x"),
        showlegend=False,
    )

    for idx, rtype in enumerate(layout):
        col = idx % 5
        row = 3 - idx // 5
        cfg = REGION_TYPE_CFG[rtype]
        dash = "dot" if rtype in (5, 6) else "solid"
        lw = 3 if rtype in (5, 6) else 2
        fig.add_shape(
            type="rect",
            x0=col + 0.05, x1=col + 0.95,
            y0=row + 0.05, y1=row + 0.95,
            fillcolor=cfg["fill"],
            line=dict(color=cfg["border"], width=lw, dash=dash),
        )
        fig.add_annotation(
            x=col + 0.5, y=row + 0.5,
            text=cfg["label"], showarrow=False,
            font=dict(family="JetBrains Mono", size=14, color=cfg["border"]),
        )

    if is_stw:
        fig.add_shape(
            type="rect", x0=0, x1=5, y0=0, y1=4,
            fillcolor="rgba(255,23,68,0.18)", line=dict(width=0),
        )
        fig.add_annotation(
            x=2.5, y=2, text="⏸ STOP-THE-WORLD", showarrow=False,
            font=dict(family="Barlow Condensed", size=28, color="white"),
        )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_heap_bars(algo, young_pct, old_pct, is_stw):
    meta_pct = 42.0
    color = algo["color"]
    labels = ["Metaspace", "Old Gen", "Young Gen"]
    values = [meta_pct, old_pct, young_pct]
    colors = []
    for i, v in enumerate(values):
        if i == 0:
            colors.append("#3A5A70")
        elif v > 76:
            colors.append("#FF5533")
        else:
            colors.append(color if i == 2 else hex_to_rgba(color, 0.8))

    annotations = []
    for i, v in enumerate(values):
        txt = f"{v:.0f}%"
        if v > 76 and i > 0:
            txt = f"⚠ {txt}"
        annotations.append(txt)

    fig = go.Figure()
    for i in range(3):
        fig.add_trace(go.Bar(
            y=[labels[i]], x=[values[i]],
            orientation="h",
            marker_color=colors[i],
            text=annotations[i],
            textposition="inside",
            textfont=dict(family="JetBrains Mono", size=11, color="#C8DDE8"),
            showlegend=False,
        ))
        fig.add_trace(go.Bar(
            y=[labels[i]], x=[100 - values[i]],
            orientation="h",
            marker_color="#0C1628",
            showlegend=False,
            text="", textposition="none",
        ))

    fig.update_layout(
        **PLOTLY_BASE,
        barmode="stack",
        width=480, height=240,
        yaxis=dict(
            tickfont=dict(family="JetBrains Mono", size=10, color="#2A4560"),
            autorange="reversed",
        ),
        xaxis=dict(visible=False, range=[0, 100]),
        bargap=0.35,
    )

    if is_stw:
        fig.add_shape(
            type="rect", x0=0, x1=100, y0=-0.5, y1=2.5,
            fillcolor="rgba(255,23,68,0.18)", line=dict(width=0),
        )
        fig.add_annotation(
            x=50, y=1, text="⏸ STOP-THE-WORLD", showarrow=False,
            font=dict(family="Barlow Condensed", size=24, color="white"),
        )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
