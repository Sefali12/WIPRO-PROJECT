"""
screenshot_util.py
-------------------
Saves a timestamped screenshot into reports/screenshots/.
Called automatically by conftest.py's pytest hook whenever a test fails,
and can also be called manually from any test/page for evidence capture.
"""

import os
from datetime import datetime


def capture_screenshot(driver, test_name: str) -> str:
    shot_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "reports",
        "screenshots",
    )
    os.makedirs(shot_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() else "_" for c in test_name)
    filepath = os.path.join(shot_dir, f"{safe_name}_{timestamp}.png")

    driver.save_screenshot(filepath)
    return filepath
