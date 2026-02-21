import os
from pathlib import Path
import pytest

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def _bool_env(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "y", "on")


@pytest.fixture(scope="session")
def settings():
    load_dotenv()  # loads .env if present

    return {
        "base_url": os.getenv("BASE_URL", "https://www.twitch.tv"),
        "headless": _bool_env("HEADLESS", "false"),
        "timeout": int(os.getenv("TIMEOUT_SECONDS", "10")),
        "mobile_device": os.getenv("MOBILE_DEVICE", "iPhone 12 Pro"),
        "reports_dir": Path("reports") / "screenshots",
    }


@pytest.fixture
def driver(settings):
    options = Options()

    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": (
            "Mozilla/5.0 (Linux; Android 12; ) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Mobile Safari/537.36"
        ),
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")

    if settings["headless"]:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)

    drv.implicitly_wait(0)
    yield drv
    drv.quit()


@pytest.fixture(scope="session", autouse=True)
def ensure_reports_dir(settings):
    settings["reports_dir"].mkdir(parents=True, exist_ok=True)

# Make screenshot if something will fail
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        settings = item.funcargs.get("settings")
        if driver and settings:
            path = settings["reports_dir"] / f"FAIL_{item.name}.png"
            driver.save_screenshot(str(path))