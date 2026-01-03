# webnavigator_ai/adapters/serper.py
import os
import requests
from typing import List
from webnavigator_ai.adapters.base import BaseSearchAdapter
from webnavigator_ai.utils.schema import NormalizedSearchResult
from webnavigator_ai.utils.logging import setup_logger

logger = setup_logger(__name__)

class SerperAdapter(BaseSearchAdapter):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        self.base = "https://google.serper.dev/search"

    def search(self, query: str) -> List[NormalizedSearchResult]:
        if not self.api_key:
            logger.info("Serper API key not found, returning empty list (mock).")
            return []
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": 10}
        resp = requests.post(self.base, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("organic", [])[:10]:
            results.append(
                NormalizedSearchResult(
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    url=item.get("link", ""),
                    source="serper",
                    published_at=item.get("published"),
                    raw=item
                )
            )
        return results
