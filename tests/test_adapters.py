from unittest.mock import MagicMock, patch
from webnavigator_ai.adapters.tavily import TavilyAdapter


@patch("webnavigator_ai.adapters.tavily.requests.post")
def test_tavily_adapter_mocked(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "results": [
            {
                "title": "Mock Result",
                "content": "Mock snippet",
                "url": "https://example.com",
            }
        ]
    }

    mock_post.return_value = mock_response

    adapter = TavilyAdapter(api_key="fake-key")
    results = adapter.search("test query")

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0].title == "Mock Result"
    assert results[0].url == "https://example.com"
