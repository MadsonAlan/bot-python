from requests import options
from src.infra.browser.SeleniumBrowser import SeleniumBrowser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import logging

class Chrome(SeleniumBrowser):
    """
    Chrome browser class to create a Chrome browser instance
    extends Browser class
    """

    def __init__(self, headless=False):
        super().__init__()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--autoplay-policy=no-user-gesture-required")
        self.options.add_argument("--mute-audio")
        if headless:
            self.options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)

    def log_page_header(self) -> None:
        try:
            title = self.driver.title
            url = self.driver.current_url
            logging.info(f"Page: {title} | URL: {url}")
        except Exception as e:
            logging.info(f"Could not read page header: {e}")
