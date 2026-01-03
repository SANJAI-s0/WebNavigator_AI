# SentinelWeb AI

---

![](docs/logo.svg)

---

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python) ![CI](https://github.com/SANJAI-s0/WebNavigator_AI/actions/workflows/ci.yml/badge.svg) ![Tests](https://img.shields.io/badge/tests-passing-brightgreen) ![Coverage](https://img.shields.io/badge/coverage-100%25-success) ![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit) ![Docker](https://img.shields.io/badge/docker-supported-blue?logo=docker) ![License](https://img.shields.io/badge/license-MIT-green) ![Status](https://img.shields.io/badge/status-stable-brightgreen) ![Version](https://img.shields.io/github/v/release/SANJAI-s0/WebNavigator_AI?label=version) ![PyPI](https://img.shields.io/pypi/v/PACKAGE_NAME?color=informational&logo=pypi)

**AI-Driven Web Automation Framework (Selenium + Real-Time Search + Agent Memory)**

WebNavigator AI is a **reusable agent-based framework** that lets an AI agent:

-   🌐 Search the web in real time
-   🧠 Reason, remember, and learn
-   🖥️ Visually control a real browser using Selenium
-   🤖 Verify information using Gemini (or heuristics)
-   📊 Run interactively via Streamlit

This is **not** a simple Selenium bot — it is a **thinking web agent**.

---

## 📑 Table of Contents

-   [🚀 Features](#-features)
-   [🧠 How It Works (High Level)](#-how-it-works-high-level)
-   [🏗 Project Structure (Updated)](#-project-structure-updated)
-   [⚙ Installation](#-installation)
    -   [Clone Repository](#1-clone-repository)
    -   [Create Virtual Environment](#2-create-virtual-environment)
    -   [Install Dependencies](#3-install-dependencies)
    -   [Editable Install](#4-install-project-in-editable-mode-recommended)
    -   [Environment Variables](#5-set-up-environment-variables)
    -   [Run Streamlit App](#5-run-streamlit-app)
-   [🧪 Running Tests](#-running-tests)
-   [🧠 Example Queries](#-example-queries)
-   [🧠 Agent Memory](#-agent-memory)
-   [🐳 Docker Support](#-docker-support)
-   [🛣 Future Enhancements](#-future-enhancements)
-   [📜 License](#-license)

---

## 🚀 Features

✔ Supervisor Agent (decision maker)  
✔ Real-time web search (Tavily / SerpAPI / Serper)  
✔ Agent memory with persistence  
✔ Visible or headless browser automation  
✔ Gemini-based truth verification (optional)  
✔ Streamlit frontend  
✔ Full test suite + CI  
✔ Docker support

---

## 🧠 How It Works (High Level)

1.  User enters a query
2.  Agent selects best search provider
3.  Search results are analyzed
4.  Agent memory is consulted (past success)
5.  Best URL is chosen
6.  Selenium opens the page **visibly**
7.  Results are verified
8.  Agent memory is reinforced

---

## 🏗 Project Structure (Updated)

```text
SentinelWeb_AI/
│
├── .github/                         # GitHub configuration & automation
│   ├── ISSUE_TEMPLATE/              # Standardized issue templates
│   │   ├── bug_report.md            # Bug report template
│   │   └── feature_request.md       # Feature request template
│   ├── workflows/
│   │   └── ci.yml                   # GitHub Actions CI (tests, install, checks)
│   └── pull_request_template.md     # Pull request guidelines
│
├── docs/                            # Documentation website (MkDocs)
│   ├── api.md                       # Public API documentation
│   ├── architecture.svg             # System architecture diagram
│   ├── index.md                     # Documentation homepage
│   ├── logo.svg                     # Project logo
│   └── usage.md                     # Usage & examples guide
│
├── tests/                           # Automated test suite
│   ├── static/
│   │   └── test_page.html           # Static HTML for Selenium DOM testing
│   ├── test_adapters.py             # Tests for search adapters
│   ├── test_memory.py               # Tests for agent memory logic
│   ├── test_selenium.py             # Tests for Selenium browser actions
│   ├── test_supervisor.py           # Tests for agent decision logic
│   └── test_verifier.py             # Tests for Gemini / heuristic verifier
│
├── webnavigator_ai/                 # Core framework package
│   ├── __init__.py                  # Package entry point
│   │
│   ├── adapters/                    # Search engine adapters
│   │   ├── __init__.py
│   │   ├── base.py                  # Base adapter + normalization
│   │   ├── serpapi.py               # SerpAPI adapter
│   │   ├── serper.py                # Serper.dev adapter
│   │   └── tavily.py                # Tavily adapter
│   │
│   ├── agent/                       # Agent intelligence layer
│   │   ├── __init__.py
│   │   ├── memory.py                # Persistent agent memory (queries/domains)
│   │   └── supervisor.py            # Supervisor agent (reasoning + orchestration)
│   │
│   ├── selenium_bot/                # Browser automation layer
│   │   ├── __init__.py
│   │   └── browser.py               # Selenium wrapper (visible/headless)
│   │
│   ├── streamlit_app/               # Frontend UI
│   │   └── app.py                   # Streamlit application entry
│   │
│   ├── utils/                       # Shared utilities
│   │   ├── logging.py               # Centralized structured logging
│   │   └── schema.py                # Data models & normalized schemas
│   │
│   └── verifier/                    # Verification layer
│       ├── __init__.py
│       └── gemini_verifier.py       # Gemini-powered + heuristic verification
│
├── .agent_memory.json               # Persistent agent memory (runtime-generated)
├── .coverage                        # Test coverage output
├── .env                             # Local environment variables (ignored)
├── .env.example                     # Example env configuration
├── .gitignore                       # Git ignore rules
│
├── ARCHITECTURE.md                  # Detailed system architecture explanation
├── CHANGELOG.md                     # Version history & release notes
├── CODE_OF_CONDUCT.md               # Community conduct guidelines
├── CONTRIBUTING.md                  # Contribution guidelines
├── Dockerfile                       # Docker build configuration
├── LICENSE                          # MIT license
├── mkdocs.yml                       # MkDocs configuration
├── pyproject.toml                   # Build system & project metadata
├── pytest.ini                       # Pytest configuration
├── README.md                        # Main project documentation
├── requirements.txt                 # Runtime dependencies
├── run_streamlit.sh                 # Helper script to launch Streamlit
└── test_memory.json                 # Test-only memory file (isolated)
```

---

## ⚙ Installation

### 1. Clone Repository

```bash
git clone https://github.com/SANJAI-s0/SentinelWeb_AI.git
cd SentinelWeb_AI
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venvScriptsactivate      # Windows
# OR
source .venv/bin/activate   # Linux / Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Project in Editable Mode (Recommended)

```bash
pip install -e .
```

> 🔎 This allows WebNavigator_AI to be used as a live, editable Python package. All code changes are reflected immediately without reinstalling. Required for clean imports, testing, and agent reusability.

### 5. Set Up Environment Variables

-   Copy `.env.example` to `.env` and fill in your API keys.

**Create a `.env` file:**

```
TAVILY_API_KEY=your_key_here
SERPAPI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

HEADLESS=false
```

> Gemini is optional — heuristic verification is used if not provided.

### 5. Run Streamlit App

**Streamlit UI**

```bash
streamlit run webnavigator_ai/streamlit_app/app.py
```

**Or using helper script**

```bashbash
./run_streamlit.sh
```

> The app will be available at `http://localhost:8501`.

---

## 🧪 Running Tests

Run the full test suite with:

```bash
pytest
```

> This will execute all tests in the `tests/` directory.

**Or Run with coverage:**

```bash
pytest --cov=webnavigator_ai
```

> This generates a coverage report. To view it in the browser, run:

```bash
coverage html
```

> Then open `htmlcov/index.html`. Make sure to install `pytest-cov` if you haven't already:

```bash
pip install pytest-cov
```

---

## 🧠 Example Queries

Try these queries in the application:

-   python selenium tutorial
-   is selenium used for web automation
-   what is github
-   how does web scraping work
-   latest ai agent frameworks

---

## 🧠 Agent Memory

The agent automatically:

-   Remembers successful URLs per query
-   Learns trusted domains
-   Stores data in `.agent_memory.json`
-   Reuses memory across sessions

> Memory is fully isolated during tests.

---

## 🐳 Docker Support

Build the Docker image:

```bash
docker build -t webnavigator_ai .
```

Run the Docker container:

```bash
docker run -d -p 8501:8501 --name webnavigator_ai_container webnavigator_ai
```

> Access the Streamlit app at `http://localhost:8501`. Make sure to set environment variables in the Dockerfile or use Docker secrets for API keys. Modify the Dockerfile as needed for your environment. For headless mode, ensure `HEADLESS=true` is set in the environment. You may need to install additional dependencies for headless Chrome in Docker. Refer to the Docker documentation for more details. Stop the container with:

```bash
docker stop webnavigator_ai_container
```

Remove the container with:

```bash
docker rm webnavigator_ai_container
```

---

## 🛣 Future Enhancements

-   ⏳ Memory decay / TTL
-   🧠 LLM-based page understanding
-   🤝 Multi-agent collaboration
-   🌐 Playwright support
-   🧪 Autonomous browsing goals

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**© 2026 Sanjai**

> Educational and development use only.

---
