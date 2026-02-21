import pytest
from pathlib import Path
import time

from ui.pages.twitch_home_page import TwitchHomePage
from ui.pages.twitch_search_page import TwitchSearchPage
from ui.pages.twitch_streamer_page import TwitchGameDirectoryPage, TwitchStreamerPage


@pytest.mark.ui
def test_twitch_starcraft_flow_mobile(driver, settings):
    base_url = settings["base_url"]
    timeout = settings["timeout"]
    screenshots_dir: Path = settings["reports_dir"]

    home = TwitchHomePage(driver, timeout=timeout)
    search = TwitchSearchPage(driver, timeout=timeout)
    directory = TwitchGameDirectoryPage(driver, timeout=timeout)
    streamer = TwitchStreamerPage(driver, timeout=timeout)

    # Test flow #
    
    # Open webpage and handle two popups
    home.open(base_url)
    home.handle_optional_popups()
    
    # Search and open game
    home.go_to_search()
    search.search("StarCraft II")
    search.open_game("StarCraft II")
    
    # Scroll 2 times (requirement)
    directory.scroll_down(times=2)
    
    # Open streamer and prepare screenshot
    directory.open_first_streamer()
    streamer.wait_loaded()
    time.sleep(1)
    streamer.screenshot(screenshots_dir / "test_twitch_screenshot.png")
