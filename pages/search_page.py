"""
search_page.py
---------------
Page Object for the header search box (present on every page of the site)
and the search results listing that follows.

search_for() is deliberately resilient: it tries clicking the search
button first, falls back to pressing Enter in the search box, and finally
falls back to navigating straight to the site's search route. Public demo
sites occasionally tweak their button markup without warning — this keeps
the test from being hostage to one exact DOM structure.
"""

from urllib.parse import quote_plus

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger(__name__)


class SearchPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='search']")
    SEARCH_BUTTON = (
        By.XPATH,
        "//*[@id='search']//button | //*[@id='search']//span[contains(@class,'input-group-btn')]//button",
    )
    PRODUCT_TILES = (By.CSS_SELECTOR, ".product-thumb")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-thumb h4 a")

    def search_for(self, product_name: str):
        log.info(f"Searching for product: '{product_name}'")
        self.type(self.SEARCH_INPUT, product_name)

        # Attempt 1: click the search button (short wait — fail fast into a fallback)
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.SEARCH_BUTTON)
            )
            btn.click()
            log.info("Search submitted via button click")
            return
        except Exception:
            log.warning("Search button not clickable — falling back to Enter key")

        # Attempt 2: press Enter inside the search box
        try:
            search_box = self.find(self.SEARCH_INPUT)
            search_box.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 3).until(
                lambda d: "search" in d.current_url.lower()
            )
            log.info("Search submitted via Enter key")
            return
        except Exception:
            log.warning("Enter key didn't navigate — falling back to direct URL")

        # Attempt 3: navigate straight to the OpenCart search route
        base = self.driver.current_url.split("index.php")[0]
        self.driver.get(f"{base}index.php?route=product/search&search={quote_plus(product_name)}")
        log.info("Search submitted via direct URL navigation")

    def get_result_count(self) -> int:
        try:
            return len(self.find_all(self.PRODUCT_TILES))
        except Exception:
            return 0

    def get_result_names(self):
        try:
            return [el.text for el in self.find_all(self.PRODUCT_NAMES)]
        except Exception:
            return []

    def has_results(self) -> bool:
        return self.get_result_count() > 0