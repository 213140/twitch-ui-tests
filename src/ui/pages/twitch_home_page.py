from selenium.webdriver.common.by import By
from .base_page import BasePage


class TwitchHomePage(BasePage):
    SEARCH_BUTTON = (By.XPATH, "//*[@id='root']/div[2]/a[2]/div/div[1]")

    def go_to_search(self) -> None:
        self.handle_optional_popups()
        self.click(*self.SEARCH_BUTTON)
        
