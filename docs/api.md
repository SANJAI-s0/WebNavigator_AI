# 🧩 API Reference — WebNavigator AI

This document describes the **public Python APIs** exposed by **WebNavigator AI**.  
These APIs allow you to programmatically control the agent, browser automation,
search adapters, memory system, and verification layer.

---

## 🧠 SupervisorAgent

### Location
```python
webnavigator_ai.agent.supervisor.SupervisorAgent
```

### Description
The `SupervisorAgent` is the central orchestrator of WebNavigator AI.  
It manages the overall workflow, including search, memory, reasoning, and navigation.

**The central orchestrator of the framework.**

The SupervisorAgent:
- Chooses the best real-time search provider 
- Analyzes search results 
- Uses memory to improve decisions 
- Selects the most relevant URL 
- Controls Selenium automation 
- Triggers verification (Gemini or heuristic)

### Constructor
```python
SupervisorAgent(
    tavily_key: str | None = None,
    serp_key: str | None = None,
    serper_key: str | None = None,
    gemini_key: str | None = None,
    headless: bool = True,
    debugger_address: str | None = None,
    chrome_user_data_dir: str | None = None
)
```

### Parameters:
```
| Parameter            | Type   | Description                       |
| -------------------- | ------ | --------------------------------- |
| tavily_key           | `str`  | Tavily API key                    |
| serp_key             | `str`  | SerpAPI key                       |
| serper_key           | `str`  | Serper.dev API key                |
| gemini_key           | `str`  | Gemini API key (optional)         |
| headless             | `bool` | Run browser headless or visible   |
| debugger_address     | `str`  | Attach to existing Chrome session |
| chrome_user_data_dir | `str`  | Use persistent Chrome profile     |
```

### run_job()
```python
run_job(
    query: str,
    steps: list[dict]
) -> dict
```
> Executes the full agent pipeline.

### Parameters:
```
| Name  | Type         | Description                 |
| ----- | ------------ | --------------------------- |
| query | `str`        | Natural language user query |
| steps | `list[dict]` | Selenium automation steps   |
```

### Returns:
```json
{
  "query": "string",
  "search_adapter_used": "string",
  "search_results": [],
  "selenium_trace": [],
  "verification": {},
  "timestamp": 1234567890.0
}
```

## 🌐 Search Adapters

All search adapters inherit from a common interface.

**Base Interface**
```python
webnavigator_ai.adapters.base.BaseSearchAdapter
```

**Supported Adapters**

- `TavilyAdapter`
- `SerpApiAdapter`
- `SerperAdapter`

### search()
```python
search(
    query: str,
    num_results: int = 5
) -> list[dict]
```
> Performs a search query and returns normalized results.

### Parameters:
```
| Name        | Type    | Description                     |
| ----------- | ------- | ------------------------------- |
| query       | `str`   | Natural language search query    |
| num_results | `int`   | Number of results to return      |
```

---
