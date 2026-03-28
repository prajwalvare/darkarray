import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Mission Control | Context Saver", layout="centered")

st.title("🚀 Mission Control")
st.subheader("Start a New Work Session")
st.markdown("Capture your context before you dive in.")

# ✅ STEP 1 FIX: Initialize session storage
if "sessions" not in st.session_state:
    st.session_state.sessions = []

# --- STEP 1: CREATE TASK / SESSION ---
with st.container(border=True):
    # Task Name
    task_name = st.text_input("What are you working on?", placeholder="e.g., Debugging Auth API")

    # Layout for Priority and Deadline
    col1, col2 = st.columns(2)
    
    with col1:
        priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Urgent"])
    
    with col2:
        has_deadline = st.checkbox("Set a deadline?")
        if has_deadline:
            deadline = st.date_input("Deadline Date")
        else:
            deadline = None

    # Notes & Next Steps
    notes = st.text_area("Initial Notes / Context", placeholder="Links, thoughts, or current blockers...")
    next_step = st.text_input("Immediate Next Step", placeholder="What's the very first thing to do?")

    # Start Button
    if st.button("▶️ Start Session", use_container_width=True, type="primary"):
        if task_name:
            start_time = datetime.now().strftime("%H:%M:%S")

            # ✅ STEP 1 FIX: Store session data
            session = {
                "task": task_name,
                "priority": priority,
                "deadline": str(deadline) if deadline else None,
                "notes": notes,
                "next_step": next_step,
                "status": "Active",
                "start_time": start_time,
                "pause_time": None
            }

            st.session_state.sessions.append(session)

            st.success(f"Session '{task_name}' started at {start_time}!")

            # Optional preview (your original idea, but now backed by real data)
            st.divider()
            st.write("### 📦 Active Context Captured")
            st.json(session)

        else:
            st.error("Please enter a task name to start.")

st.divider()
st.header("🟢 Active Session")

# Find active sessions
active_sessions = [s for s in st.session_state.sessions if s["status"] == "Active"]

if active_sessions:
    current = active_sessions[-1]

    st.success(f"Currently Working On: {current['task']}")

    col1, col2 = st.columns(2)
    col1.metric("Started At", current["start_time"])
    col2.metric("Priority", current["priority"])

    st.write("📝 **Notes:**", current["notes"])
    st.write("➡️ **Next Step:**", current["next_step"])

else:
    st.info("No active session")

# -------------------------

st.divider()
st.header("📊 All Sessions")

if st.session_state.sessions:
    df = pd.DataFrame(st.session_state.sessions)
    st.dataframe(df, use_container_width=True)
else:
    st.write("No sessions created yet.")
# --- FOOTER ---
st.caption("Astitva Hackathon 2025 | Solving the Context-Switch Tax")