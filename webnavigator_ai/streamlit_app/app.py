# webnavigator_ai/streamlit_app/app.py
import os
import json
import streamlit as st

from webnavigator_ai.agent.supervisor import SupervisorAgent
from webnavigator_ai.utils.logging import setup_logger

logger = setup_logger(__name__)

st.set_page_config(page_title="WebNavigator AI", layout="wide")
st.title("WebNavigator AI — Selenium + Real-time Search + Gemini Verifier")

# -------------------------------------------------------------------
# Sidebar configuration
# -------------------------------------------------------------------
with st.sidebar:
    st.header("Configuration")

    # Automation mode: visible, attach, headless
    automation_mode = st.selectbox(
        "Automation mode",
        [
            "Visible Chrome (Selenium launches Chrome)",
            "Attach to running Chrome (remote debugging)",
            "Headless (no browser shown)"
        ],
        index=0,
        help="Choose how Selenium will run. Attach mode requires starting Chrome with --remote-debugging-port."
    )

    headless = automation_mode == "Headless (no browser shown)"

    # If attach, ask for debugger address / profile path
    debugger_address = ""
    user_data_dir = ""
    if automation_mode == "Attach to running Chrome (remote debugging)":
        debugger_address = st.text_input("Chrome debugger address (host:port)", value=os.getenv("CHROME_DEBUGGER_ADDRESS", "127.0.0.1:9222"))
        user_data_dir = st.text_input("Optional Chrome user-data-dir (to use a profile)", value=os.getenv("CHROME_USER_DATA_DIR", ""))

    tavily_key = st.text_input("Tavily API Key", value=os.getenv("TAVILY_API_KEY", ""), type="password")
    serpapi_key = st.text_input("SerpApi Key", value=os.getenv("SERPAPI_API_KEY", ""), type="password")
    serper_key = st.text_input("Serper API Key", value=os.getenv("SERPER_API_KEY", ""), type="password")
    gemini_key = st.text_input("Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password")
    hide_trace = st.checkbox("Hide Selenium automation trace in UI (show visual browser only)", value=True)
    st.markdown("---")
    st.caption("If using Attach mode: start Chrome with --remote-debugging-port=9222. See README section in UI for details.")

# -------------------------------------------------------------------
# Main input
# -------------------------------------------------------------------
query = st.text_input("Search query", value="python selenium tutorial")
start = st.button("Start automation job")

# -------------------------------------------------------------------
# Run job
# -------------------------------------------------------------------
if start:
    st.info("Starting job... (the browser may open or be controlled)")

    steps = [
        {"action": "open", "url": "https://duckduckgo.com"},
        {"action": "type", "selector": "input[name='q']", "text": query},
        {"action": "press", "key": "ENTER", "sleep": 1.5},
    ]

    # Create the agent with automation options
    agent = SupervisorAgent(
        tavily_key=tavily_key or None,
        serp_key=serpapi_key or None,
        serper_key=serper_key or None,
        gemini_key=gemini_key or None,
        headless=headless,
        debugger_address=debugger_address or None,
        chrome_user_data_dir=user_data_dir or None
    )

    status = st.empty()

    try:
        status.text("Running agent, search, and Selenium automation...")
        res = agent.run_job(query, steps)
        status.success("Job complete.")
    except Exception as e:
        logger.exception("Job failed")
        st.error(f"Job failed: {e}")
        st.stop()

    # ------------------------------------------------------------
    # Render results (Selenium trace suppressed if hide_trace True)
    # ------------------------------------------------------------
    if not hide_trace:
        st.subheader("Selenium automation trace")
        st.json(res.get("selenium_trace", []))
    else:
        st.subheader("Selenium automation")
        st.info("Automation was performed in your selected browser. Steps trace is hidden as requested.")

    st.subheader("Search adapter used & real-time results")
    st.write(f"Adapter used: **{res.get('search_adapter_used')}**")
    st.json(res.get("search_results", [])[:8])

    st.subheader("Gemini verification summary")
    verification = res.get("verification", {})
    st.write(verification.get("summary", "No summary available"))
    st.json(verification)

    st.subheader("Final structured output (JSON)")
    # If hiding selenium trace, replace with a human-friendly message
    final_out = dict(res)
    if hide_trace:
        final_out["selenium_trace"] = "visualized-in-browser"
    st.code(json.dumps(final_out, indent=2))
