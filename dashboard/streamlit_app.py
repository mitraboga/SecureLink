import os

import streamlit as st

from dashboard.api_client import fetch_events, fetch_summary, login

API_BASE_URL = os.getenv("SECURELINK_API_URL", "http://api:8000")

st.set_page_config(page_title="SecureLink Dashboard", layout="wide")
st.title("SecureLink Security Dashboard")

with st.sidebar:
    st.header("API Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            st.session_state["token"] = login(username, password, API_BASE_URL)
        except Exception:
            st.error("Login failed")

token = st.session_state.get("token")
if not token:
    st.info("Log in to view security events.")
    st.stop()

try:
    summary = fetch_summary(token, API_BASE_URL)
    events = fetch_events(token, API_BASE_URL)
except Exception:
    st.error("Unable to load dashboard data.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total Events", summary["total_events"])
col2.metric("High Severity", summary["by_severity"].get("HIGH", 0))
col3.metric("Replay Attempts", summary["by_event_type"].get("REPLAY_ATTACK_DETECTED", 0))

st.subheader("Event Types")
st.bar_chart(summary["by_event_type"])

st.subheader("Recent Security Events")
st.dataframe(events, use_container_width=True)
