"""
base_page.py
------------
Parent class for every Page Object. Centralizes explicit waits and common
interactions so individual page classes stay short and only declare
locators + business actions (this is the heart of the POM pattern).
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config_reader import get_config
from utils.logger import get_logger

log = get_logger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, get_config().get("explicit_wait", 15))

    def open(self, url: str):
        log.info(f"Navigating to {url}")
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.find_clickable(locator).click()

    def type(self, locator, text: str):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def is_displayed(self, locator) -> bool:
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def title(self) -> str:
        return self.driver.title
