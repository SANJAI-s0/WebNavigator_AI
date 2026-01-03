# webnavigator_ai/verifier/gemini_verifier.py
import os
import requests
from typing import List, Dict, Any

from webnavigator_ai.utils.schema import NormalizedSearchResult
from webnavigator_ai.utils.logging import setup_logger

logger = setup_logger(__name__)


class GeminiVerifier:
    """
    Gemini-based verifier with heuristic fallback.
    Supports Gemini 2.5 Flash via v1beta:generateContent.
    """

    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_url = api_url or os.getenv(
            "GEMINI_API_URL",
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def verify_claims(self, results: List[NormalizedSearchResult]) -> Dict[str, Any]:
        """
        Returns:
        {
            "verdicts": [{"url":..., "verdict": "...", "confidence": 0.82}, ...],
            "confidence": float,
            "summary": str
        }
        """
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set. Using heuristic verifier.")
            return self._heuristic_verify(results)

        # Build prompt
        prompt = self._build_prompt(results)

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,  # REQUIRED for Gemini v1beta
        }

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 300,
            },
        }

        try:
            resp = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()

            # Safely extract Gemini text output
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )

            if not text:
                raise ValueError("Empty Gemini response")

            verdicts = [
                {"url": r.url, "verdict": "unknown", "confidence": 0.5}
                for r in results[:8]
            ]

            return {
                "verdicts": verdicts,
                "confidence": 0.5,
                "summary": text.strip(),
            }

        except Exception as e:
            logger.warning(
                "Gemini API call failed, falling back to heuristic: %s", e
            )
            return self._heuristic_verify(results)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _build_prompt(self, results: List[NormalizedSearchResult]) -> str:
        lines = [
            "You are a fact-checking assistant.",
            "Evaluate the credibility and consensus of the following web search results.",
            "Provide a short summary of whether the information appears reliable.\n",
        ]

        for i, r in enumerate(results[:8], 1):
            lines.append(
                f"{i}. Title: {r.title}\n"
                f"   URL: {r.url}\n"
                f"   Snippet: {r.snippet}\n"
            )

        return "\n".join(lines)

    def _heuristic_verify(self, results: List[NormalizedSearchResult]) -> Dict[str, Any]:
        verdicts = []

        for r in results[:8]:
            u = r.url or ""

            if any(
                domain in u
                for domain in (
                    "wikipedia.org",
                    ".gov",
                    ".edu",
                    "bbc.co",
                    "nytimes.com",
                )
            ):
                verdict = "likely-true"
                conf = 0.85
            else:
                verdict = "uncertain"
                conf = 0.45

            verdicts.append(
                {"url": u, "verdict": verdict, "confidence": conf}
            )

        overall_conf = (
            sum(v["confidence"] for v in verdicts) / len(verdicts)
            if verdicts
            else 0.0
        )

        summary = (
            f"Local heuristic: evaluated {len(verdicts)} results. "
            "Mostly uncertain without Gemini verification."
        )

        return {
            "verdicts": verdicts,
            "confidence": round(overall_conf, 2),
            "summary": summary,
        }
