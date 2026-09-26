
# Selenium Python Automation Framework
**Unittest + PyTest + Page Object Model | E-Commerce Login & Search**

A scalable, production-style UI test automation framework built for
`https://tutorialsninja.com/demo/` (an OpenCart-based e-commerce demo site).

## Why this framework, not just a script

Anyone can write a linear script that opens a browser and clicks buttons.
This repo demonstrates the things a real automation engineer is actually
hired for:

| Capability | Where |
|---|---|
| Page Object Model (no locators in test files) | `pages/` |
| Two test runners on one shared POM layer | `tests/test_*_pytest.py` + `tests/test_*_unittest.py` |
| Centralized configuration (no hardcoded URLs/timeouts) | `config/config.yaml` + `utils/config_reader.py` |
| Data-driven testing from CSV | `data/test_data.csv` + `utils/csv_reader.py` |
| Dynamic test data generation (Faker) | account registration in both test suites |
| Automatic screenshot-on-failure | `utils/screenshot_util.py` + `tests/conftest.py` hook |
| Centralized logging (console + file) | `utils/logger.py` |
| Self-contained HTML test report | `pytest-html`, auto-generated in `reports/` |
| Driver lifecycle management | `utils/driver_factory.py` |

## Project structure

```
├── config/
│   └── config.yaml            # base_url, browser, headless, timeouts
├── pages/                     # Page Object Model
│   ├── base_page.py           # shared wait/click/type helpers
│   ├── register_page.py
│   ├── login_page.py
│   └── search_page.py
├── utils/
│   ├── driver_factory.py      # builds WebDriver from config
│   ├── config_reader.py
│   ├── csv_reader.py
│   ├── screenshot_util.py
│   └── logger.py
├── data/
│   └── test_data.csv          # search terms for data-driven tests
├── tests/
│   ├── conftest.py            # pytest fixtures + failure-screenshot hook
│   ├── test_login_search_pytest.py
│   └── test_login_search_unittest.py
├── reports/                   # generated: HTML report, screenshots, logs
├── requirements.txt
├── pytest.ini
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You need **Google Chrome** installed. `webdriver-manager` downloads the
matching ChromeDriver automatically on first run — no manual driver setup.

## Running the tests

```bash
# Full PyTest suite (generates reports/pytest_report.html)
pytest

# Just the fast smoke test
pytest -m smoke

# Just the data-driven regression suite
pytest -m regression

# The Unittest suite
python -m unittest tests.test_login_search_unittest -v
```

After a run, open **`reports/pytest_report.html`** in a browser — this is
the artifact worth showing on camera / attaching to your submission.

## Design notes

- **Why the tests register a new account instead of using fixed
  credentials:** a public demo site's test accounts get reset or
  rate-limited. Generating a fresh account via `Faker` on every run makes
  the suite self-contained and repeatable with zero manual setup —
  register → login → search, no pre-existing login required.
- **Why `name=` selectors instead of `id=`:** OpenCart-based demo themes
  change `id` attributes more often than `name` attributes across
  versions. All locators live in one page class each, so if the live site
  markup ever drifts, there is exactly one file to update per page —
  that isolation is the entire point of POM.
- **headless: false in config.yaml** is intentional for the demo
  recording — flip it to `true` for CI.

## What each capstone requirement maps to

- Unittest ✅ `tests/test_login_search_unittest.py`
- PyTest ✅ `tests/test_login_search_pytest.py`
- POM ✅ `pages/`
- Utility classes ✅ `utils/`
- Configuration management ✅ `config/config.yaml`
- Test data handling (CSV) ✅ `data/test_data.csv`
- Screenshots on failure ✅ `tests/conftest.py` hook + `unittest`'s `tearDown`
- HTML reporting ✅ `pytest-html` self-contained report
