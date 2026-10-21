import os
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = ROOT / "reports" / "screenshots"


@pytest.fixture
def driver():
    options = Options()
    is_codespace = bool(os.getenv("CODESPACES")) or bool(os.getenv("CODESPACE_NAME"))
    if os.getenv("HEADLESS", "0") == "1" or (os.name != "nt" and (is_codespace or not os.getenv("DISPLAY"))):
        options.add_argument("--headless=new")
    if os.name != "nt":
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)
    try:
        yield browser
    finally:
        # Optional viewing time without stdin/input errors under pytest capture.
        # PowerShell: $env:BROWSER_HOLD_SECONDS="15"
        try:
            hold_seconds = max(0.0, float(os.getenv("BROWSER_HOLD_SECONDS", "0")))
        except ValueError:
            hold_seconds = 0.0
        if hold_seconds:
            print(f"Keeping Chrome open for {hold_seconds:g} seconds...")
            time.sleep(hold_seconds)
        browser.quit()


@pytest.fixture
def screenshot(driver, request):
    def capture(label):
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{request.node.name}_{label}.png"
        driver.save_screenshot(str(SCREENSHOT_DIR / filename))
    return capture


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser is not None:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            try:
                browser.save_screenshot(str(SCREENSHOT_DIR / f"{item.name}_FAILED.png"))
            except Exception:
                pass
