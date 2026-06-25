import streamlit as st


def render_metrics_row(algo, phase, is_stw, young_pct, old_pct, cycles):
    cols = st.columns(6)
    with cols[0]:
        st.metric("GC CYCLES", cycles)
    with cols[1]:
        st.metric("PHASE", phase["name"])
    with cols[2]:
        st.metric("APP THREADS", "PAUSED" if is_stw else f"{phase['app_t']} active")
    with cols[3]:
        st.metric("GC THREADS", f"{phase['gc_t']} active")
    with cols[4]:
        st.metric("YOUNG GEN", f"{young_pct:.0f}%")
    with cols[5]:
        st.metric("OLD GEN", f"{old_pct:.0f}%")
