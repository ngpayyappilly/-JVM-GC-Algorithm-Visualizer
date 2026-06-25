import streamlit as st
import plotly.graph_objects as go
from styles import PLOTLY_BASE


def render_thread_panel(phase, algo_color):
    app_t = phase["app_t"]
    gc_t = phase["gc_t"]
    is_stw = phase["stw"]

    labels = [f"gc-{i}" for i in range(7, -1, -1)] + [f"app-{i}" for i in range(3, -1, -1)]
    values = []
    colors = []

    for i in range(7, -1, -1):
        active = i < gc_t
        values.append(1.0 if active else 0.15)
        colors.append(algo_color + "99" if active else "#0C1628")

    for i in range(3, -1, -1):
        active = i < app_t
        if is_stw:
            values.append(0.15)
            colors.append("#200508")
        else:
            values.append(1.0 if active else 0.15)
            colors.append("#1A4A7A" if active else "#0C1628")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=values,
        orientation="h",
        marker_color=colors,
        showlegend=False,
        text=["PAUSED" if is_stw and l.startswith("app") else "" for l in labels],
        textposition="inside",
        textfont=dict(family="JetBrains Mono", size=8, color="#FF5555"),
    ))

    fig.update_layout(
        **PLOTLY_BASE,
        height=280,
        xaxis=dict(visible=False, range=[0, 1.1]),
        yaxis=dict(
            tickfont=dict(family="JetBrains Mono", size=9, color="#2A4560"),
        ),
        bargap=0.25,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
