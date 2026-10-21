import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = ROOT / "reports" / "screenshots"


@pytest.fixture
def driver():
    options = Options()

    # Mở Chrome với giao diện trên Windows
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)

    try:
        yield browser
    finally:
        input("Đã hoàn thành test. Nhấn Enter để đóng Chrome...")
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
