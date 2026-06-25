import streamlit as st


def lerp(a: float, b: float, t: float) -> float:
    t = max(0.0, min(1.0, t))
    return a + (b - a) * t


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def init_sim_state():
    defaults = {
        "algo_key": "g1gc",
        "playing": True,
        "speed": 1.0,
        "phase_idx": 0,
        "tick": 0,
        "cycles": 0,
        "young_pct": 18.0,
        "old_pct": 10.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def advance_tick(algo_data: dict) -> None:
    s = st.session_state
    if not s.playing:
        return
    phase = algo_data["phases"][s.phase_idx]
    t = s.tick / max(phase["ticks"], 1)
    s.young_pct = clamp(lerp(phase["yd"][0], phase["yd"][1], t), 5.0, 95.0)
    s.old_pct = clamp(lerp(phase["od"][0], phase["od"][1], t), 5.0, 95.0)
    s.tick += 1
    if s.tick >= phase["ticks"]:
        s.tick = 0
        next_idx = (s.phase_idx + 1) % len(algo_data["phases"])
        if next_idx == 0:
            s.cycles += 1
        s.phase_idx = next_idx


def reset_sim(algo_key: str, algo_data: dict) -> None:
    st.session_state.algo_key = algo_key
    st.session_state.phase_idx = 0
    st.session_state.tick = 0
    st.session_state.cycles = 0
    p = algo_data["phases"][0]
    st.session_state.young_pct = p["yd"][0]
    st.session_state.old_pct = p["od"][0]
