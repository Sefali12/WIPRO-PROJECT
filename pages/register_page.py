"""
register_page.py
-----------------
Page Object for the "Register" page.

Why registration is part of this framework: the login test needs a real
account, and hardcoding one fake credential pair is fragile (gets banned/
changed on a public demo site). So the suite creates a fresh account with
random data on every run via Faker, then logs in with it immediately after.

is_registration_successful() checks the URL rather than reading page text —
OpenCart's success page can auto-redirect shortly after load, and reading
DOM text right as that happens causes a StaleElementReferenceException.
Checking the URL avoids touching any element that might disappear under us.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger(__name__)


class RegisterPage(BasePage):
    REGISTER_URL_PATH = "index.php?route=account/register"

    FIRST_NAME = (By.CSS_SELECTOR, "input[name='firstname']")
    LAST_NAME = (By.CSS_SELECTOR, "input[name='lastname']")
    EMAIL = (By.CSS_SELECTOR, "input[name='email']")
    TELEPHONE = (By.CSS_SELECTOR, "input[name='telephone']")
    PASSWORD = (By.CSS_SELECTOR, "input[name='password']")
    CONFIRM_PASSWORD = (By.CSS_SELECTOR, "input[name='confirm']")
    AGREE_CHECKBOX = (By.CSS_SELECTOR, "input[name='agree']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "input[value='Continue']")

    def navigate(self, base_url: str):
        self.open(base_url.rstrip("/") + "/" + self.REGISTER_URL_PATH)

    def register_new_account(self, first_name, last_name, email, telephone, password):
        log.info(f"Registering new account for {email}")
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.EMAIL, email)
        self.type(self.TELEPHONE, telephone)
        self.type(self.PASSWORD, password)
        self.type(self.CONFIRM_PASSWORD, password)
        self.click(self.AGREE_CHECKBOX)
        self.click(self.CONTINUE_BUTTON)

    def is_registration_successful(self) -> bool:
        try:
            self.wait.until(
                lambda d: "route=account/success" in d.current_url
                or "route=account/account" in d.current_url
            )
            log.info(f"Registration confirmed via URL: {self.driver.current_url}")
            return True
        except Exception:
            log.error(f"Registration not confirmed. Current URL: {self.driver.current_url}")
            return False
