from __future__ import annotations
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)
        self.driver.delete_all_cookies()
        #self.driver.refresh()

    def click(self, by, value: str) -> None:
        try:
            el = self.wait.until(EC.element_to_be_clickable((by, value)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            el.click()
        except TimeoutException as e:
            current = self.driver.current_url
            raise TimeoutException(
                f"Timeout waiting for element to be clickable.\n"
                f"Locator: ({by}, {value})\n"
                f"URL: {current}"
            ) from e

    def type(self, by: By, value: str, text: str, clear: bool = True) -> None:
        el = self.wait.until(EC.visibility_of_element_located((by, value)))
        if clear:
            el.clear()
        el.send_keys(text)

    def scroll_down(self, times: int = 1) -> None:
        for _ in range(times):
            self.driver.execute_script("window.scrollBy(0, Math.floor(window.innerHeight * 0.9));")
            # tiny wait so content loads
            self.wait.until(lambda d: True)

    def screenshot(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(path))

    def handle_optional_popups(self) -> None:
        short = WebDriverWait(self.driver, 2)

        # Keep using web
        try:
            keep_web = short.until(
                EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Keep using web']"))
            )
            keep_web.click()
        except TimeoutException:
            pass

        # Consent accept
        try:
            accept = short.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-a-target='consent-banner-accept']"))
            )
            accept.click()
        except TimeoutException:
            pass
        

