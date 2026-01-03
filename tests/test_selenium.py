from unittest.mock import MagicMock, patch
from webnavigator_ai.selenium_bot.browser import SeleniumBot


@patch.object(SeleniumBot, "_resolve_chromedriver", return_value="dummy-path")
@patch("webnavigator_ai.selenium_bot.browser.webdriver.Chrome")
def test_selenium_open_step(mock_chrome, mock_resolve):
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver

    bot = SeleniumBot(headless=True)

    steps = [{"action": "open", "url": "https://example.com"}]
    trace = bot.run_steps(steps)

    assert isinstance(trace, list)
    assert trace[0]["action"] == "open"
    assert trace[0]["result"] == "success"
