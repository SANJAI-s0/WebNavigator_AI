#!/usr/bin/env bash
set -e

echo "🚀 Starting WebNavigator AI (Streamlit)..."

export PYTHONPATH=.

streamlit run webnavigator_ai/streamlit_app/app.py

# Make executable on Linux/macOS:

chmod +x run_streamlit.sh
