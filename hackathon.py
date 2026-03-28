import streamlit as st
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

# --- FOOTER ---
st.caption("Astitva Hackathon 2025 | Solving the Context-Switch Tax")