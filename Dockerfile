FROM python:3.12-slim

# ----------------------------
# System dependencies
# ----------------------------
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# ----------------------------
# App setup
# ----------------------------
WORKDIR /app

COPY pyproject.toml README.md ./
COPY webnavigator_ai ./webnavigator_ai
COPY tests ./tests

RUN pip install --upgrade pip \
    && pip install -e .[dev]

# ----------------------------
# Streamlit config
# ----------------------------
EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV PYTHONPATH=/app
ENV SELENIUM_HEADLESS=true

# ----------------------------
# Start app
# ----------------------------
CMD ["streamlit", "run", "webnavigator_ai/streamlit_app/app.py"]
