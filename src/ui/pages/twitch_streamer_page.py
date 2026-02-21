from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class TwitchGameDirectoryPage(BasePage):
    FIRST_STREAMER_LINK = (
        By.XPATH,
        "(//div[contains(@class,'InjectLayout') and @role='list']//article)[1] //button[contains(@class,'ScCoreLink')]"
    )

    def open_first_streamer(self) -> None:
        self.handle_optional_popups()

        before = self.driver.current_url
        self.click(*self.FIRST_STREAMER_LINK)

        # Check if we navigated away from directory
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != before)


class TwitchStreamerPage(BasePage):
    BODY = (By.TAG_NAME, "body")
    ANY_MAINISH = (By.CSS_SELECTOR, "[role='main'], main, #root, #app, body")

    def wait_loaded(self) -> None:
        self.handle_optional_popups()

        wait = WebDriverWait(self.driver, 20)

        # 1) Wait for navigation to a streamer URL)
        wait.until(lambda d: (
            "/directory/" not in d.current_url
            and "/search" not in d.current_url
            and "twitch.tv" in d.current_url
        ))

        # 2) Page should at least render a body + root-ish container
        wait.until(EC.presence_of_element_located(self.BODY))
        wait.until(EC.presence_of_element_located(self.ANY_MAINISH))

        # 3) Popups can appear late
        self.handle_optional_popups()