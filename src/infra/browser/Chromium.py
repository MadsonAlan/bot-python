from src.infra.browser.SeleniumBrowser import SeleniumBrowser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import logging

class Chromium(SeleniumBrowser):
    """
    Chromium browser class to create a Chromium browser instance
    extends Browser class
    """

    def __init__(self, headless):
        super().__init__()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--no-sandbox")
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-background-networking")
        self.options.add_argument("--disable-sync")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-default-apps")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-first-run")
        self.options.add_argument("--no-service-autorun")
        self.options.add_argument("--disable-gcm")
        self.options.add_argument("--autoplay-policy=no-user-gesture-required")
        self.options.add_argument("--mute-audio")
        self.options.binary_location = "/usr/bin/chromium"
        service = ChromeService("/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=self.options)

    def log_page_header(self) -> None:
        try:
            title = self.driver.title
            url = self.driver.current_url
            logging.info(f"Page: {title} | URL: {url}")
        except Exception as e:
            logging.info(f"Could not read page header: {e}")
