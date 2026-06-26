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
        .block-container { padding-top: 1rem !important; max-width: 1200px; }
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
        .stw-banner {
            background: rgba(255,23,68,0.15);
            border: 1px solid rgba(255,23,68,0.5);
            border-radius: 6px;
            padding: 10px 18px;
            text-align: center;
            margin-bottom: 8px;
            animation: stw-pulse 1.2s ease-in-out infinite;
        }
        @keyframes stw-pulse {
            0%, 100% { box-shadow: 0 0 8px rgba(255,23,68,0.3); }
            50% { box-shadow: 0 0 20px rgba(255,23,68,0.6); }
        }
        .algo-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 4px;
        }
        .algo-header-name {
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 28px;
            font-weight: 900;
            letter-spacing: 0.08em;
        }
        .algo-header-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 3px 10px;
            border-radius: 4px;
            letter-spacing: 0.05em;
        }
        .region-legend {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            padding: 4px 0;
        }
        .region-legend-item {
            display: flex;
            align-items: center;
            gap: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            color: #9BBFCC;
        }
        .region-legend-swatch {
            width: 12px;
            height: 12px;
            border-radius: 2px;
            border-width: 1.5px;
            border-style: solid;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: #060D1C;
            border-bottom: 1px solid #102040;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 11px !important;
            letter-spacing: 0.08em;
            color: #2A4560 !important;
            padding: 8px 20px !important;
        }
        .stTabs [aria-selected="true"] {
            color: #C8DDE8 !important;
        }
    </style>
    """, unsafe_allow_html=True)
