# 🧠 WebNavigator AI – Architecture

## Overview
WebNavigator AI is an **agent-based web automation framework** that combines:

- Real-time web search
- Autonomous reasoning
- Persistent memory
- Visual browser control

---

## Core Components

### Streamlit UI
- User interaction layer
- Displays results
- Controls execution flow

### SupervisorAgent
- Central orchestrator
- Chooses search adapter
- Applies memory + heuristics
- Decides final navigation

### AgentMemory
- Stores successful query → URL mappings
- Reinforces trusted domains
- Persists across sessions

### Search Adapters
- Tavily
- SerpAPI
- Serper
- Normalized results

### SeleniumBot
- Controls real Chrome browser
- Headless or visible
- User-observable automation

### Verifier
- Gemini-based verification (optional)
- Heuristic fallback

---

## Design Principles

- Deterministic
- Testable
- Extensible
- Human-visible automation
- No hidden scraping
