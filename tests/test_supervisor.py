from webnavigator_ai.agent.supervisor import SupervisorAgent
from webnavigator_ai.utils.schema import NormalizedSearchResult


def test_supervisor_agent_selects_url_by_keyword(monkeypatch):
    agent = SupervisorAgent(
        tavily_key=None,
        serp_key=None,
        serper_key=None,
        gemini_key=None,
    )

    # 🔒 CRITICAL: disable memory recall for this test
    if hasattr(agent, "memory"):
        monkeypatch.setattr(agent.memory, "recall_query", lambda _: None)

    results = [
        NormalizedSearchResult(
            title="Python Selenium Tutorial",
            snippet="Learn Selenium",
            url="https://example.com/selenium",
            source="test",
        ),
        NormalizedSearchResult(
            title="Other Result",
            snippet="Other",
            url="https://other.com",
            source="test",
        ),
    ]

    selected = agent._select_click_url(results, "python selenium tutorial")

    assert selected == "https://example.com/selenium"
