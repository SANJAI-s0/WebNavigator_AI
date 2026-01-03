# webnavigator_ai/adapters/serpapi.py
import os
import requests
from typing import List
from webnavigator_ai.adapters.base import BaseSearchAdapter
from webnavigator_ai.utils.schema import NormalizedSearchResult
from webnavigator_ai.utils.logging import setup_logger

logger = setup_logger(__name__)

class SerpApiAdapter(BaseSearchAdapter):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        self.base = "https://serpapi.com/search.json"

    def search(self, query: str) -> List[NormalizedSearchResult]:
        if not self.api_key:
            logger.info("SerpApi API key not found, returning empty list (mock).")
            return []
        params = {"q": query, "api_key": self.api_key, "num": 10}
        resp = requests.get(self.base, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("organic_results", [])[:10]:
            results.append(
                NormalizedSearchResult(
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    url=item.get("link", ""),
                    source="serpapi",
                    published_at=item.get("date"),
                    raw=item
                )
            )
        return results
