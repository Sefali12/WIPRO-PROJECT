"""
driver_factory.py
------------------
Single place responsible for creating and configuring the WebDriver.
Tests / fixtures never call `webdriver.Chrome()` directly — they call
DriverFactory.get_driver() so browser choice, headless mode, window size
and implicit waits are all controlled from config.yaml.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.config_reader import get_config
from utils.logger import get_logger

log = get_logger(__name__)


class DriverFactory:
    @staticmethod
    def get_driver():
        config = get_config()
        browser = config.get("browser", "chrome").lower()
        headless = config.get("headless", False)
        window_size = config.get("window_size", "1920,1080")

        log.info(f"Launching browser='{browser}' headless={headless}")

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument(f"--window-size={window_size}")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options,
            )
        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(
                service=__import__(
                    "selenium.webdriver.firefox.service", fromlist=["Service"]
                ).Service(GeckoDriverManager().install()),
                options=options,
            )
        else:
            raise ValueError(f"Unsupported browser in config.yaml: {browser}")

        driver.implicitly_wait(config.get("implicit_wait", 10))
        if not headless:
            driver.maximize_window()
        return driver
