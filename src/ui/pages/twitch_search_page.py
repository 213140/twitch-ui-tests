from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage


class TwitchSearchPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], input[aria-label='Search']")
    GAME_RESULT = (By.XPATH, "//a[contains(@href,'/directory/category') or contains(@href,'/directory/game')][1]")

    def search(self, text: str) -> None:
        self.type(*self.SEARCH_INPUT, text=text)
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)

    def open_game(self, game_name: str = "StarCraft II") -> None:
        self.click(*self.GAME_RESULT)
