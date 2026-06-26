import streamlit as st
from algorithms import ALGORITHMS
from simulation import init_sim_state, advance_tick, reset_sim
from styles import inject_global_styles, hex_to_rgba
from components.heap_view import render_heap
from components.thread_panel import render_thread_panel
from components.phase_ribbon import render_phase_ribbon
from components.metrics_row import render_metrics_row

st.set_page_config(
    page_title="JVM GC Algorithm Visualizer",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()
init_sim_state()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ JVM GC VISUALIZER")
    st.caption("Platform Engineering / SRE")
    st.divider()

    st.markdown("**ALGORITHM**")
    algo_keys = list(ALGORITHMS.keys())
    algo_labels = {k: f"{ALGORITHMS[k]['name']}  —  {ALGORITHMS[k]['badge']}" for k in algo_keys}

    selected_key = st.radio(
        label="Select GC Algorithm",
        options=algo_keys,
        format_func=lambda k: algo_labels[k],
        index=algo_keys.index(st.session_state.algo_key),
        label_visibility="collapsed",
    )
    if selected_key != st.session_state.algo_key:
        reset_sim(selected_key, ALGORITHMS[selected_key])
        st.rerun()

    st.divider()
    st.markdown("**SIMULATION CONTROLS**")
    col_play, col_reset = st.columns(2)
    with col_play:
        if st.button("⏸ PAUSE" if st.session_state.playing else "▶ PLAY", use_container_width=True):
            st.session_state.playing = not st.session_state.playing
    with col_reset:
        if st.button("↺ RESET", use_container_width=True):
            reset_sim(st.session_state.algo_key, ALGORITHMS[st.session_state.algo_key])

    st.markdown("**SPEED**")
    speed_options = [0.5, 1.0, 2.0, 4.0]
    current_speed = st.session_state.get("speed", 1.0)
    speed_idx = speed_options.index(current_speed) if current_speed in speed_options else 1
    speed = st.radio(
        label="Simulation Speed",
        options=speed_options,
        format_func=lambda s: f"{s}×",
        index=speed_idx,
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.speed = speed

    st.divider()
    with st.expander("Platform Context"):
        st.code(
            "Pod:    4 GiB / 4000m CPU\n"
            "Heap:   ~3,273 MiB (Paketo)\n"
            "Threads: 50 (BPL)\n"
            "OTel:   Java Agent (OTLP)\n"
            "GC:     -XX:+UseG1GC\n"
            "        -XX:MaxGCPauseMillis=150\n"
            "        -XX:IHOP=40\n"
            "        -XX:ActiveProcessorCount=4",
            language="yaml",
        )


# ── Helpers ──────────────────────────────────────────────────
def render_algo_header(algo):
    color = algo["color"]
    st.markdown(
        f'<div class="algo-header">'
        f'<span class="algo-header-name" style="color:{color}">{algo["name"]}</span>'
        f'<span class="algo-header-label" style="background:{hex_to_rgba(color, 0.15)};'
        f'border:1px solid {hex_to_rgba(color, 0.4)};color:{color}">{algo["label"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_algo_card(algo):
    color = algo["color"]
    metrics = algo["metrics"]
    warn_pause = algo["name"] in ("ParallelGC", "SerialGC")
    items = [("PAUSES", metrics["pause"]), ("CPU COST", metrics["cpu"]),
             ("THROUGHPUT", metrics["throughput"]), ("HEAP RANGE", metrics["heap"])]
    grid = "".join(
        f'<div style="background:#060D1C;border:1px solid #102040;border-radius:4px;padding:6px 8px">'
        f'<div style="font-family:\'JetBrains Mono\';font-size:8px;color:#2A4560;letter-spacing:0.1em;margin-bottom:2px">{k}</div>'
        f'<div style="font-family:\'Barlow Condensed\';font-size:13px;font-weight:700;'
        f'color:{"#FF5533" if k == "PAUSES" and warn_pause else "#C8DDE8"}">{v}</div></div>'
        for k, v in items
    )
    st.markdown(
        f'<div style="background:#081224;border:1px solid #102040;border-radius:8px;padding:14px">'
        f'<div style="font-family:\'JetBrains Mono\';font-size:9px;color:{color};letter-spacing:0.15em;font-weight:700;margin-bottom:8px">{algo["badge"]}</div>'
        f'<p style="font-family:\'Barlow Condensed\';font-size:12px;color:#9BBFCC;line-height:1.5;margin-bottom:10px">{algo["insight"]}</p>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">{grid}</div></div>',
        unsafe_allow_html=True,
    )


def render_phase_description(algo, phase, progress, is_stw):
    border_color = "#FF1744" if is_stw else algo["color"]
    badge_text = "STOP-THE-WORLD" if is_stw else "CONCURRENT"
    st.markdown(
        f'<div style="border-left:3px solid {border_color};padding:12px 16px;background:#060D1C;border-radius:0 8px 8px 0;margin-top:8px">'
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">'
        f'<span style="font-family:\'Barlow Condensed\';font-size:14px;font-weight:800;color:{border_color}">{phase["name"]}</span>'
        f'<span style="font-family:\'JetBrains Mono\';font-size:9px;padding:2px 8px;border:1px solid {hex_to_rgba(border_color, 0.27)};border-radius:3px;color:{border_color}">{badge_text}</span>'
        f'<div style="flex:1;height:2px;background:#102040;border-radius:1px"><div style="height:100%;width:{progress:.0f}%;background:{border_color};border-radius:1px"></div></div>'
        f'<span style="font-family:\'JetBrains Mono\';font-size:9px;color:#2A4560">{progress:.0f}%</span></div>'
        f'<p style="font-family:\'Barlow Condensed\';font-size:15px;color:#9BBFCC;line-height:1.55;margin:0">{phase["desc"]}</p></div>',
        unsafe_allow_html=True,
    )


# ── Algorithm header ─────────────────────────────────────────
algo = ALGORITHMS[st.session_state.algo_key]
render_algo_header(algo)

# ── Tabs ─────────────────────────────────────────────────────
tab_viz, tab_details = st.tabs(["VISUALIZATION", "ALGORITHM DETAILS"])

with tab_details:
    render_algo_card(algo)
    st.markdown("---")
    st.markdown(
        f'<p style="font-family:\'Barlow Condensed\';font-size:14px;color:#2A4560;margin-top:8px">'
        f'PHASE LIFECYCLE — {len(algo["phases"])} phases per cycle</p>',
        unsafe_allow_html=True,
    )
    for i, p in enumerate(algo["phases"]):
        border = "#FF1744" if p["stw"] else algo["color"]
        tag = "STW" if p["stw"] else "CONC"
        st.markdown(
            f'<div style="border-left:2px solid {border};padding:6px 12px;margin:4px 0;background:#060D1C;border-radius:0 4px 4px 0">'
            f'<span style="font-family:\'JetBrains Mono\';font-size:10px;color:{border};font-weight:700">{i+1}. {p["name"]}</span>'
            f'<span style="font-family:\'JetBrains Mono\';font-size:8px;padding:1px 6px;margin-left:8px;border:1px solid {hex_to_rgba(border, 0.3)};border-radius:3px;color:{border}">{tag}</span>'
            f'<br><span style="font-family:\'Barlow Condensed\';font-size:12px;color:#9BBFCC">{p["desc"]}</span></div>',
            unsafe_allow_html=True,
        )


# ── Main animated fragment ───────────────────────────────────
def get_run_every():
    return 0.05 / st.session_state.get("speed", 1.0)


with tab_viz:
    @st.fragment(run_every=get_run_every())
    def animated_visualization():
        algo = ALGORITHMS[st.session_state.algo_key]
        advance_tick(algo)
        phase = algo["phases"][st.session_state.phase_idx]
        is_stw = phase["stw"]
        progress = (st.session_state.tick / max(phase["ticks"], 1)) * 100

        stw_container = st.empty()
        if is_stw:
            stw_container.markdown(
                '<div class="stw-banner">'
                '<span style="font-family:\'Barlow Condensed\';font-size:22px;font-weight:900;'
                'color:#FF1744;letter-spacing:0.15em">⏸  STOP-THE-WORLD PAUSE ACTIVE</span><br>'
                '<span style="font-family:\'JetBrains Mono\';font-size:10px;color:#FF5555">'
                'ALL APPLICATION THREADS SUSPENDED — NO REQUESTS PROCESSED</span></div>',
                unsafe_allow_html=True,
            )

        render_phase_ribbon(algo, st.session_state.phase_idx, progress)

        col_heap, col_right = st.columns([3, 1.5])
        with col_heap:
            render_heap(algo, phase, st.session_state.young_pct, st.session_state.old_pct, is_stw)
        with col_right:
            render_thread_panel(phase, algo["color"])

        render_metrics_row(algo, phase, is_stw,
                           st.session_state.young_pct,
                           st.session_state.old_pct,
                           st.session_state.cycles)

        render_phase_description(algo, phase, progress, is_stw)

    animated_visualization()
