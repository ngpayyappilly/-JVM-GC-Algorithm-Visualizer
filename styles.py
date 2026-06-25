import streamlit as st

COLORS = {
    "bg": "#03070F",
    "surface": "#060D1C",
    "card": "#081224",
    "border": "#102040",
    "text": "#9BBFCC",
    "dim": "#2A4560",
    "bright": "#C8DDE8",
    "stw_red": "#FF1744",
    "stw_bg": "rgba(255,23,68,0.11)",
}

ALGO_COLORS = {
    "g1gc": "#00C8FF",
    "zgc": "#00FF88",
    "shenandoah": "#FFB800",
    "parallelgc": "#FF5533",
    "serialgc": "#9B8FFF",
}

PLOTLY_BASE = dict(
    paper_bgcolor="#060D1C",
    plot_bgcolor="#060D1C",
    font=dict(family="JetBrains Mono, monospace", color="#9BBFCC"),
    margin=dict(l=0, r=0, t=0, b=0),
)


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def inject_global_styles():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap">
    <style>
        .stApp { background-color: #03070F; }
        .stSidebar, [data-testid="stSidebar"] { background-color: #060D1C !important; }
        .block-container { padding-top: 1rem !important; }
        [data-testid="stMetric"] {
            background: #081224;
            border: 1px solid #102040;
            border-radius: 6px;
            padding: 8px 12px;
        }
        [data-testid="stMetricLabel"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 10px !important;
            color: #2A4560 !important;
            letter-spacing: 0.1em;
        }
        [data-testid="stMetricValue"] {
            font-family: 'Barlow Condensed', sans-serif !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #9BBFCC !important;
        }
        .stRadio label {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 12px !important;
            color: #9BBFCC !important;
        }
        .stButton button {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 11px !important;
            letter-spacing: 0.1em;
            border-radius: 6px;
        }
        .js-plotly-plot { background: transparent !important; }
        h1, h2, h3 {
            font-family: 'Barlow Condensed', sans-serif !important;
            letter-spacing: 0.08em;
        }
    </style>
    """, unsafe_allow_html=True)
