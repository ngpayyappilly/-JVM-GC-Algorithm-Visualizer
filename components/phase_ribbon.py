import streamlit as st
import plotly.graph_objects as go
from styles import PLOTLY_BASE, hex_to_rgba


def render_phase_ribbon(algo, phase_idx, progress):
    phases = algo["phases"]
    color = algo["color"]
    fig = go.Figure()

    x_pos = 0
    for i, p in enumerate(phases):
        w = p["ticks"]
        is_active = i == phase_idx
        if p["stw"]:
            fill = "rgba(255,23,68,0.5)" if is_active else "rgba(255,23,68,0.2)"
        else:
            fill = hex_to_rgba(color, 0.53 if is_active else 0.2)

        fig.add_shape(
            type="rect",
            x0=x_pos, x1=x_pos + w, y0=0, y1=1,
            fillcolor=fill,
            line=dict(color=color if is_active else "#102040", width=2 if is_active else 1),
        )

        if is_active:
            prog_w = w * progress / 100
            fig.add_shape(
                type="rect",
                x0=x_pos, x1=x_pos + prog_w, y0=0, y1=0.18,
                fillcolor=color, line=dict(width=0),
            )

        if w > 8:
            label = p["name"][:10]
            if p["stw"] and w > 14:
                label = "STW " + label[:6]
            fig.add_annotation(
                x=x_pos + w / 2, y=0.55,
                text=label, showarrow=False,
                font=dict(family="JetBrains Mono", size=8,
                          color="#C8DDE8" if is_active else "#2A4560"),
            )
        x_pos += w

    fig.update_layout(
        **PLOTLY_BASE,
        height=70,
        xaxis=dict(visible=False, range=[0, x_pos]),
        yaxis=dict(visible=False, range=[0, 1]),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
