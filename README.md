# twitch-ui-tests
Automated UI testing with Python - target (Twitch)
[https://m.twitch.tv/]

## How to run locally
1. Clone repository
2. Create virtualenv (`python -m venv .venv`) and activate venv
3. Install dependencies (`pip install -r requirements.txt`)
4. Copy `.env.example` -> `.env`
5. Run: `pytest -m ui -v`


## WEB UI Test Flow

## Web UI Test Flow – Twitch Mobile (StarCraft II)
| Step | Action | Page Object | Description | Expected Result |
|------|--------|-------------|-------------|-----------------|
| 1 | Open website | `TwitchHomePage` | Navigate to base URL (`https://m.twitch.tv`) | Twitch mobile homepage loads successfully |
| 2 | Handle popups | `TwitchHomePage` | Close "Keep using web" and cookie consent popups (if present) | No blocking popups remain |
| 3 | Open search | `TwitchHomePage` | Click search icon in header | Search input page is displayed |
| 4 | Enter game name | `TwitchSearchPage` | Type **"StarCraft II"** and submit search | Search results are shown |
| 5 | Open game directory | `TwitchSearchPage` | Click first matching game result | StarCraft II directory page opens |
| 6 | Scroll page | `TwitchGameDirectoryPage` | Scroll down twice (project requirement) | Additional live stream cards become visible |
| 7 | Open first streamer | `TwitchGameDirectoryPage` | Click first available live streamer | Streamer channel page opens |
| 8 | Wait for page load | `TwitchStreamerPage` | Wait until navigation completes and page is fully loaded | Streamer page is ready |
| 9 | Take screenshot | `TwitchStreamerPage` | Capture screenshot of streamer page | Screenshot saved in `reports/screenshots/` |

## ⚠️ Note About Popup Handling

When opening Twitch mobile, two initial popups may appear:
- "Keep using web" prompt  
- Cookie consent banner  
These are handled by the `handle_optional_popups()` method implemented in `BasePage`, which safely detects and closes them before continuing the test flow.

![Test Execution Demo](docs/demo_twitch_ui.gif)