import time
from typing import List, Dict, Any

from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
)

from webnavigator_ai.adapters.tavily import TavilyAdapter
from webnavigator_ai.adapters.serpapi import SerpApiAdapter
from webnavigator_ai.adapters.serper import SerperAdapter
from webnavigator_ai.selenium_bot.browser import SeleniumBot
from webnavigator_ai.verifier.gemini_verifier import GeminiVerifier
from webnavigator_ai.agent.memory import AgentMemory
from webnavigator_ai.utils.logging import setup_logger
from webnavigator_ai.utils.schema import NormalizedSearchResult

logger = setup_logger(__name__)


class SupervisorAgent:
    """
    SupervisorAgent
    ----------------
    Responsibilities:
    - Choose best search adapter (Tavily → SerpAPI → Serper)
    - Analyze search results
    - Decide best URL (agent reasoning + memory)
    - Drive Selenium visibly (or headless / real user browser)
    - Verify results using Gemini or heuristics
    """

    def __init__(
        self,
        tavily_key: str | None = None,
        serp_key: str | None = None,
        serper_key: str | None = None,
        gemini_key: str | None = None,
        headless: bool = True,
        debugger_address: str | None = None,
        chrome_user_data_dir: str | None = None,
    ):
        self.tavily = TavilyAdapter(api_key=tavily_key)
        self.serpapi = SerpApiAdapter(api_key=serp_key)
        self.serper = SerperAdapter(api_key=serper_key)
        self.verifier = GeminiVerifier(api_key=gemini_key)

        self.headless = headless
        self.debugger_address = debugger_address
        self.chrome_user_data_dir = chrome_user_data_dir

        # 🧠 Persistent memory
        self.memory = AgentMemory()

    # ------------------------------------------------------------------
    # Search adapter selection
    # ------------------------------------------------------------------
    def _choose_adapter(self):
        if self.tavily.api_key:
            return self.tavily
        if self.serpapi.api_key:
            return self.serpapi
        if self.serper.api_key:
            return self.serper
        return self.serper  # free-tier fallback

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception),
    )
    def _call_search(self, adapter, query: str) -> List[NormalizedSearchResult]:
        logger.info(
            "Calling search adapter: %s for query: %s",
            adapter.__class__.__name__,
            query,
        )
        results = adapter.search(query)
        if results is None:
            raise RuntimeError("Search adapter returned None")
        return results

    # ------------------------------------------------------------------
    # 🧠 AGENT DECISION LOGIC (Memory + Reasoning)
    # ------------------------------------------------------------------
    def _select_click_url(
        self,
        results: List[NormalizedSearchResult],
        query: str,
    ) -> str | None:
        """
        Decide which URL is best for the query.

        Priority:
        0. Agent memory hit
        1. Keyword match
        2. Trusted learning domains
        3. First result fallback
        """
        if not results:
            return None

        # 0️⃣ MEMORY HIT
        remembered = self.memory.recall_query(query)
        if remembered:
            logger.info("Agent memory hit for query '%s': %s", query, remembered)
            return remembered

        keywords = [k.lower() for k in query.split()]

        # 1️⃣ Keyword match
        for r in results:
            haystack = f"{r.title} {r.url}".lower()
            if any(k in haystack for k in keywords):
                logger.info("Agent selected URL by keyword match: %s", r.url)
                return r.url

        # 2️⃣ Trusted domains
        trusted_domains = (
            "docs",
            "readthedocs",
            "tutorial",
            "learn",
            "selenium",
            "python",
            "github.com",
            "geeksforgeeks",
            "w3schools",
            "realpython",
        )

        for r in results:
            if any(d in r.url.lower() for d in trusted_domains):
                logger.info("Agent selected URL by trusted domain: %s", r.url)
                return r.url

        # 3️⃣ Fallback
        logger.info("Agent fallback URL: %s", results[0].url)
        return results[0].url

    # ------------------------------------------------------------------
    # Main job runner
    # ------------------------------------------------------------------
    def run_job(
        self,
        query: str,
        steps: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Full pipeline:
        - Search (with fallback)
        - Agent selects best URL (memory-aware)
        - Selenium navigates directly (visual & robust)
        - Gemini verification
        """

        adapter = self._choose_adapter()

        # ---------------- Search ----------------
        try:
            search_results = self._call_search(adapter, query)
        except Exception as e:
            logger.exception("Primary search failed: %s", e)
            search_results = []

        # Fallback adapters
        if not search_results:
            tried = {adapter.__class__.__name__}
            for cand in (self.tavily, self.serpapi, self.serper):
                if cand.__class__.__name__ in tried:
                    continue
                try:
                    search_results = self._call_search(cand, query)
                    if search_results:
                        adapter = cand
                        break
                except Exception:
                    continue

        # ---------------- Agent decision ----------------
        selected_url = self._select_click_url(search_results, query)

        final_steps = list(steps)

        # ✅ Robust navigation (no SERP DOM dependency)
        if selected_url:
            final_steps.append(
                {
                    "action": "open",
                    "url": selected_url,
                    "sleep": 1.5,
                }
            )

            # 🧠 Store memory
            self.memory.remember_query(query, selected_url)
            self.memory.reinforce_domain(selected_url)

        # ---------------- Selenium execution ----------------
        browser = SeleniumBot(
            headless=self.headless,
            debugger_address=self.debugger_address,
            chrome_user_data_dir=self.chrome_user_data_dir,
        )

        selenium_trace = browser.run_steps(final_steps)

        # ---------------- Verification ----------------
        verification = self.verifier.verify_claims(search_results)

        return {
            "query": query,
            "search_adapter_used": adapter.__class__.__name__,
            "search_results": [r.to_dict() for r in search_results],
            "selenium_trace": selenium_trace,
            "verification": verification,
            "timestamp": time.time(),
        }
