"""
login_page.py
--------------
Page Object for the "Login" page.

navigate() is defensive: OpenCart auto-logs a customer in immediately after
registration, so visiting /account/login while already logged in silently
redirects straight to /account/account instead of showing the login form.
If that happens, this logs out first so login() always starts from a real,
fresh login form.

login() is defensive in two more ways:
1. If the login button isn't clickable for any reason, it falls back to
   pressing Enter in the password field to submit the form.
2. After submitting, it WAITS for either a redirect to the account page or
   a visible error message before returning — checking immediately is a
   race condition, since the browser redirect after form submission is
   asynchronous and takes a moment to complete.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger(__name__)


class LoginPage(BasePage):
    LOGIN_URL_PATH = "index.php?route=account/login"
    LOGOUT_URL_PATH = "index.php?route=account/logout"

    EMAIL = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")

    def navigate(self, base_url: str):
        self.base_url = base_url.rstrip("/") + "/"
        self.open(self.base_url + self.LOGIN_URL_PATH)

        if "account/account" in self.driver.current_url:
            log.info("Already logged in from registration — logging out for a clean login test")
            self.open(self.base_url + self.LOGOUT_URL_PATH)
            self.open(self.base_url + self.LOGIN_URL_PATH)

    def login(self, email: str, password: str):
        log.info(f"Logging in as {email}")
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)

        submitted = False
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.LOGIN_BUTTON)
            )
            btn.click()
            submitted = True
        except Exception:
            log.warning("Login button not clickable — falling back to Enter key")

        if not submitted:
            try:
                self.find(self.PASSWORD).send_keys(Keys.RETURN)
            except Exception:
                log.error("Could not submit login form by any method")

        # Wait for the outcome instead of checking immediately.
        try:
            self.wait.until(
                lambda d: "account/account" in d.current_url or self._error_visible()
            )
        except Exception:
            pass

    def _error_visible(self) -> bool:
        try:
            return self.driver.find_element(*self.ERROR_ALERT).is_displayed()
        except Exception:
            return False

    def is_logged_in(self) -> bool:
        return "account/account" in self.driver.current_url

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_ALERT) if self.is_displayed(self.ERROR_ALERT) else ""
