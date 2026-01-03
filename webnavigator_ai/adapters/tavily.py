# webnavigator_ai/adapters/tavily.py
import os
import requests
from typing import List
from webnavigator_ai.adapters.base import BaseSearchAdapter
from webnavigator_ai.utils.schema import NormalizedSearchResult
from webnavigator_ai.utils.logging import setup_logger

logger = setup_logger(__name__)


class TavilyAdapter(BaseSearchAdapter):
    """
    Tavily Search Adapter
    Official API: https://docs.tavily.com/
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.endpoint = "https://api.tavily.com/search"

    def search(self, query: str) -> List[NormalizedSearchResult]:
        if not self.api_key:
            logger.warning("Tavily API key not found. Skipping Tavily.")
            return []

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": 5
        }

        try:
            resp = requests.post(self.endpoint, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.exception("Tavily request failed: %s", e)
            return []

        results = []
        for item in data.get("results", []):
            results.append(
                NormalizedSearchResult(
                    title=item.get("title", ""),
                    snippet=item.get("content", ""),
                    url=item.get("url", ""),
                    source="tavily",
                    raw=item
                )
            )

        return results
