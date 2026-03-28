import streamlit as st
import pandas as pd
from datetime import datetime, date

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mission Control",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  – dark space theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0b0f1a;
    color: #e2e8f0;
}

/* App background */
.stApp {
    background: radial-gradient(ellipse at 20% 0%, #1a1f3a 0%, #0b0f1a 60%);
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 780px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 1px solid #1e2540;
    margin-bottom: 2rem;
}
.hero h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #818cf8, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
.hero p {
    color: #64748b;
    font-size: 0.95rem;
    margin: 0;
}

/* ── Section headers ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 0.75rem;
}

/* ── Stat pill ── */
.stat-pill {
    display: inline-block;
    background: #1e2540;
    border: 1px solid #2d3561;
    border-radius: 999px;
    padding: 0.3rem 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
}

/* ── Active session card ── */
.active-card {
    background: linear-gradient(135deg, #0f1635 0%, #131b35 100%);
    border: 1px solid #3b4fd8;
    border-radius: 16px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 40px rgba(99, 102, 241, 0.12);
}
.active-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #818cf8, #38bdf8);
    border-radius: 16px 16px 0 0;
}
.active-card h3 {
    font-family: 'Space Mono', monospace;
    font-size: 1.2rem;
    color: #e2e8f0;
    margin: 0 0 0.3rem;
}
.active-card .meta { color: #64748b; font-size: 0.85rem; }
.pulse {
    display: inline-block;
    width: 8px; height: 8px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 1.4s infinite;
    vertical-align: middle;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(1.5); }
}

/* ── Paused session card ── */
.paused-card {
    background: #111827;
    border: 1px solid #1f2a40;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.75rem;
}
.paused-card h4 {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: #cbd5e1;
    margin: 0 0 0.25rem;
}
.paused-card .meta { color: #475569; font-size: 0.82rem; }

/* ── Priority badge ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-Low      { background: #1c2b1c; color: #4ade80; }
.badge-Medium   { background: #1f2937; color: #facc15; }
.badge-High     { background: #2d1b1b; color: #f97316; }
.badge-Urgent   { background: #2d1b1b; color: #ef4444; }

/* ── Overdue card ── */
.overdue-card {
    background: #1c1010;
    border: 1px solid #450a0a;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    color: #fca5a5;
    font-size: 0.9rem;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #111827 !important;
    border: 1px solid #1f2a40 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(129,140,248,0.15) !important;
}
label, .stSelectbox label, .stTextInput label { color: #94a3b8 !important; font-size: 0.85rem !important; }

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.35) !important;
}

/* Secondary button */
.stButton > button:not([kind="primary"]) {
    background: #1e2540 !important;
    color: #94a3b8 !important;
    border: 1px solid #2d3561 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: #252d52 !important;
    color: #e2e8f0 !important;
    border-color: #818cf8 !important;
}

/* Checkbox */
.stCheckbox > label { color: #94a3b8 !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #1f2a40;
    border-radius: 12px;
    padding: 1rem;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-family: 'Space Mono', monospace !important; }

/* Dataframe */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* Alert / success */
.stSuccess { background: #0f2618 !important; border: 1px solid #166534 !important; border-radius: 10px !important; }
.stInfo    { background: #0c1a2e !important; border: 1px solid #1e3a5f !important; border-radius: 10px !important; }
.stError   { background: #1c1010 !important; border: 1px solid #450a0a !important; border-radius: 10px !important; }
.stWarning { background: #1a1500 !important; border: 1px solid #713f12 !important; border-radius: 10px !important; }

/* Divider */
hr { border-color: #1e2540 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
if "sessions" not in st.session_state:
    st.session_state.sessions = []

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🚀 Mission Control</h1>
    <p>Capture context. Stay focused. Never lose your place.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TOP STATS
# ─────────────────────────────────────────────
total    = len(st.session_state.sessions)
active   = sum(1 for s in st.session_state.sessions if s["status"] == "Active")
paused   = sum(1 for s in st.session_state.sessions if s["status"] == "Paused")
done     = sum(1 for s in st.session_state.sessions if s.get("completed"))

st.markdown(f"""
<div>
    <span class="stat-pill">📋 {total} Total</span>
    <span class="stat-pill">🟢 {active} Active</span>
    <span class="stat-pill">⏸ {paused} Paused</span>
    <span class="stat-pill">✅ {done} Done</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SECTION 1 — CREATE SESSION
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">01 — New Session</div>', unsafe_allow_html=True)

with st.container(border=True):
    task_name = st.text_input("Task Name", placeholder="e.g. Debugging Auth API")

    notes     = st.text_area("Context / Notes", placeholder="What do you know so far? Any blockers?", height=90)
    next_step = st.text_input("Immediate Next Step", placeholder="e.g. Check error log line 42")

    col1, col2 = st.columns(2)
    with col1:
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
    with col2:
        has_deadline = st.checkbox("Set Deadline")
        if has_deadline:
            deadline = st.date_input("Deadline", min_value=date.today())
        else:
            deadline = None

    if st.button("▶  Start Session", use_container_width=True, type="primary"):
        if task_name.strip():
            for s in st.session_state.sessions:
                if s["status"] == "Active":
                    s["status"] = "Paused"
                    s["pause_time"] = datetime.now().strftime("%H:%M")

            st.session_state.sessions.append({
                "task":       task_name.strip(),
                "priority":   priority,
                "deadline":   str(deadline) if deadline else None,
                "notes":      notes,
                "next_step":  next_step,
                "status":     "Active",
                "start_time": datetime.now().strftime("%H:%M:%S"),
                "pause_time": None,
                "completed":  False,
            })
            st.success(f"✦  Session **{task_name}** is now active.")
            st.rerun()
        else:
            st.error("Please enter a task name to continue.")

# ─────────────────────────────────────────────
#  SECTION 2 — ACTIVE SESSION
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">02 — Active Session</div>', unsafe_allow_html=True)

active_sessions = [s for s in st.session_state.sessions if s["status"] == "Active"]

if active_sessions:
    cur = active_sessions[-1]
    badge_class = f"badge-{cur['priority']}"
    dl_text     = f"  ·  Due {cur['deadline']}" if cur["deadline"] else ""

    st.markdown(f"""
    <div class="active-card">
        <div style="margin-bottom:0.75rem;">
            <span class="pulse"></span>
            <span style="font-size:0.78rem;color:#22c55e;font-family:'Space Mono',monospace;letter-spacing:1px;">LIVE</span>
            &nbsp;&nbsp;
            <span class="badge {badge_class}">{cur['priority']}</span>
        </div>
        <h3>{cur['task']}</h3>
        <div class="meta">Started {cur['start_time']}{dl_text}</div>
        <hr style="border-color:#1e2540;margin:1rem 0;">
        <div style="font-size:0.88rem;color:#94a3b8;margin-bottom:0.5rem;">
            <b style="color:#64748b;">Notes</b><br>{cur['notes'] or '—'}
        </div>
        <div style="font-size:0.88rem;color:#94a3b8;margin-top:0.75rem;">
            <b style="color:#64748b;">Next Step</b><br>
            <span style="color:#818cf8;">➜ {cur['next_step'] or '—'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("✏️  Update notes before pausing"):
        updated_notes = st.text_area("Notes", value=cur["notes"], key="upd_notes", height=80)
        updated_next  = st.text_input("Next Step", value=cur["next_step"], key="upd_next")

        if st.button("⏸  Pause & Save Context", use_container_width=True):
            cur["status"]     = "Paused"
            cur["pause_time"] = datetime.now().strftime("%H:%M")
            cur["notes"]      = updated_notes
            cur["next_step"]  = updated_next
            st.success("Context saved. Session paused.")
            st.rerun()
else:
    st.markdown("""
    <div style="text-align:center;padding:2rem;color:#334155;
                border:1px dashed #1e2540;border-radius:14px;">
        <div style="font-size:2rem;margin-bottom:0.5rem;">🌙</div>
        No active session — start one above.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SECTION 3 — PAUSED SESSIONS / RESUME
# ─────────────────────────────────────────────
paused_sessions = [s for s in st.session_state.sessions if s["status"] == "Paused"]

if paused_sessions:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">03 — Paused  ·  Resume a Session</div>', unsafe_allow_html=True)

    for i, session in enumerate(paused_sessions):
        badge_class = f"badge-{session['priority']}"
        with st.container(border=True):
            col_info, col_btn1, col_btn2 = st.columns([3, 1, 1])

            with col_info:
                st.markdown(f"""
                <div>
                    <span class="badge {badge_class}">{session['priority']}</span>
                    &nbsp;
                    <b style="font-size:1rem;color:#cbd5e1;">{session['task']}</b>
                </div>
                <div style="color:#475569;font-size:0.82rem;margin-top:0.3rem;">
                    Paused {session.get('pause_time','—')}
                </div>
                <div style="color:#64748b;font-size:0.83rem;margin-top:0.5rem;">
                    ➜ {session.get('next_step') or '—'}
                </div>
                """, unsafe_allow_html=True)

            with col_btn1:
                st.write("")
                if st.button("▶ Resume", key=f"res_{i}", use_container_width=True):
                    for s in st.session_state.sessions:
                        if s["status"] == "Active":
                            s["status"]     = "Paused"
                            s["pause_time"] = datetime.now().strftime("%H:%M")
                    session["status"] = "Active"
                    st.rerun()

            with col_btn2:
                st.write("")
                if st.button("✅ Done", key=f"fin_{i}", use_container_width=True):
                    session["completed"] = True
                    session["status"]    = "Completed"
                    st.rerun()

# ─────────────────────────────────────────────
#  SECTION 4 — ALL SESSIONS TABLE
# ─────────────────────────────────────────────
if st.session_state.sessions:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">04 — Session Log</div>', unsafe_allow_html=True)

    df = pd.DataFrame(st.session_state.sessions)[
        ["task", "priority", "status", "start_time", "pause_time", "deadline", "next_step"]
    ].rename(columns={
        "task":       "Task",
        "priority":   "Priority",
        "status":     "Status",
        "start_time": "Started",
        "pause_time": "Paused At",
        "deadline":   "Deadline",
        "next_step":  "Next Step",
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
#  SECTION 5 — PRODUCTIVITY STATS
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">05 — Productivity</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Sessions Today",  total)
col2.metric("Completed",       done)
col3.metric("In Progress",     active + paused)

if done >= 3:
    st.success("🏆 Focus Master — you're on a roll!")
elif done >= 1:
    st.info(f"💡 {done} task done. Keep going!")

# ─────────────────────────────────────────────
#  SECTION 6 — OVERDUE REMINDERS
# ─────────────────────────────────────────────
today   = str(date.today())
overdue = [s for s in st.session_state.sessions if s["deadline"] and s["deadline"] < today and not s.get("completed")]

if overdue:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">⚠️  Overdue</div>', unsafe_allow_html=True)
    for s in overdue:
        st.markdown(f"""
        <div class="overdue-card">
            ⚠️  <b>{s['task']}</b> was due {s['deadline']}
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#1e2540;font-family:'Space Mono',monospace;font-size:0.7rem;letter-spacing:2px;">
    ASTITVA HACKATHON 2025  ·  CONTEXT-SWITCH TAX
</div>
""", unsafe_allow_html=True)