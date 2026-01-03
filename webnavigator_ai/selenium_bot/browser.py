# webnavigator_ai/selenium_bot/browser.py
import time
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs, unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from webnavigator_ai.utils.logging import setup_logger
from webnavigator_ai.utils.schema import timestamp_iso

logger = setup_logger(__name__)


class SeleniumBot:
    def __init__(
        self,
        headless: bool = True,
        implicit_wait: int = 5,
        debugger_address: Optional[str] = None,
        chrome_user_data_dir: Optional[str] = None,
    ):
        """
        debugger_address: if provided, connect to an existing Chrome with remote debugging (host:port).
        chrome_user_data_dir: optional path to a Chrome profile directory when launching Chrome.
        """
        self.headless = headless
        self.implicit_wait = implicit_wait
        self.debugger_address = debugger_address
        self.chrome_user_data_dir = chrome_user_data_dir
        self.driver = None

    def _resolve_chromedriver(self) -> str:
        raw_path = Path(ChromeDriverManager().install())
        if raw_path.name.lower() == "chromedriver.exe":
            return str(raw_path)
        parent_dir = raw_path.parent
        exe = parent_dir / "chromedriver.exe"
        if exe.exists():
            return str(exe)
        for p in parent_dir.rglob("chromedriver.exe"):
            return str(p)
        raise RuntimeError(f"Could not locate chromedriver.exe in {parent_dir}")

    def _init_driver(self):
        chrome_options = Options()

        # If connecting to an existing Chrome via remote debugging, set debugger address
        if self.debugger_address:
            # Connect to running Chrome (user must start Chrome with --remote-debugging-port)
            chrome_options.add_experimental_option("debuggerAddress", self.debugger_address)
        else:
            # If launching, control whether headless or visible
            if self.headless:
                chrome_options.add_argument("--headless=new")
            # optional user data dir to reuse a profile
            if self.chrome_user_data_dir:
                chrome_options.add_argument(f"--user-data-dir={self.chrome_user_data_dir}")

        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver_path = self._resolve_chromedriver()
        logger.info("Using ChromeDriver: %s", driver_path)

        service = ChromeService(executable_path=driver_path)
        # When using debuggerAddress, chromedriver will attach to existing Chrome
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(self.implicit_wait)

    # run_steps as before (Keeps click_dynamic / uddg handling)
    def run_steps(self, steps: List[Dict]) -> List[Dict]:
        trace: List[Dict] = []

        try:
            self._init_driver()

            for step in steps:
                ts = timestamp_iso()
                action = step.get("action")

                try:
                    # OPEN
                    if action == "open":
                        self.driver.get(step["url"])
                        trace.append({
                            "action": "open",
                            "selector": step["url"],
                            "timestamp": ts,
                            "result": "success"
                        })

                    # TYPE
                    elif action == "type":
                        el = self.driver.find_element(By.CSS_SELECTOR, step["selector"])
                        el.clear()
                        el.send_keys(step.get("text", ""))
                        trace.append({
                            "action": "type",
                            "selector": step["selector"],
                            "timestamp": ts,
                            "result": "success"
                        })

                    # PRESS
                    elif action == "press":
                        key = step.get("key", "ENTER").upper()
                        body = self.driver.find_element(By.TAG_NAME, "body")
                        body.send_keys(getattr(Keys, key, Keys.ENTER))
                        trace.append({
                            "action": "press",
                            "selector": key,
                            "timestamp": ts,
                            "result": "success"
                        })

                    # AGENT-DECIDED CLICK (DuckDuckGo-safe)
                    elif action == "click_dynamic":
                        target_url = step["url"]
                        target_domain = urlparse(target_url).netloc.replace("www.", "")

                        links = self.driver.find_elements(By.CSS_SELECTOR, "a[href]")
                        clicked = False

                        for link in links:
                            href = link.get_attribute("href") or ""

                            # handle DuckDuckGo redirect pattern with uddg parameter
                            if "uddg=" in href:
                                try:
                                    parsed = parse_qs(urlparse(href).query)
                                    decoded = unquote(parsed.get("uddg", [""])[0])
                                except Exception:
                                    decoded = ""

                                if target_domain and target_domain in decoded:
                                    self.driver.execute_script(
                                        "arguments[0].scrollIntoView({block:'center'});",
                                        link
                                    )
                                    time.sleep(0.4)
                                    try:
                                        link.click()
                                    except Exception:
                                        self.driver.execute_script("arguments[0].click();", link)

                                    trace.append({
                                        "action": "click_dynamic",
                                        "selector": decoded,
                                        "timestamp": ts,
                                        "result": "success"
                                    })
                                    clicked = True
                                    break

                            # fallback: if link href directly contains domain
                            elif target_domain and target_domain in href:
                                self.driver.execute_script(
                                    "arguments[0].scrollIntoView({block:'center'});",
                                    link
                                )
                                time.sleep(0.4)
                                try:
                                    link.click()
                                except Exception:
                                    self.driver.execute_script("arguments[0].click();", link)

                                trace.append({
                                    "action": "click_dynamic",
                                    "selector": href,
                                    "timestamp": ts,
                                    "result": "success"
                                })
                                clicked = True
                                break

                        if not clicked:
                            raise RuntimeError(f"No DuckDuckGo result matched target domain: {target_domain}")

                    # UNKNOWN
                    else:
                        trace.append({
                            "action": action,
                            "selector": "",
                            "timestamp": ts,
                            "result": "unknown-action"
                        })

                    time.sleep(step.get("sleep", 0.8))

                except Exception as e:
                    logger.exception("Selenium step failed")
                    trace.append({
                        "action": action,
                        "selector": step.get("url", step.get("selector", "")),
                        "timestamp": ts,
                        "result": "failure",
                        "error": str(e)
                    })

            return trace

        finally:
            # only quit chromedriver if we launched Chrome; when attaching to user's Chrome,
            # quitting the driver won't close the browser but will stop chromedriver session.
            if self.driver:
                try:
                    self.driver.quit()
                except Exception:
                    pass
