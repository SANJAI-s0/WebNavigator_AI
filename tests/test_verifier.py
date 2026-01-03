from webnavigator_ai.verifier.gemini_verifier import GeminiVerifier
from webnavigator_ai.utils.schema import NormalizedSearchResult


def test_heuristic_verifier_without_api_key():
    verifier = GeminiVerifier(api_key=None)

    results = [
        NormalizedSearchResult(
            title="Wikipedia",
            snippet="Selenium info",
            url="https://en.wikipedia.org/wiki/Selenium",
            source="test",
        )
    ]

    output = verifier.verify_claims(results)

    assert "verdicts" in output
    assert output["confidence"] >= 0.5
    assert output["verdicts"][0]["verdict"] in ("likely-true", "uncertain", "unknown")
