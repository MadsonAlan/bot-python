from src.infra.browser.SeleniumBrowser import SeleniumBrowser
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver


class Firefox(SeleniumBrowser):
    """
    Firefox browser class to create a Firefox browser instance
    extends Browser class
    """

    def __init__(self, headless=False):
        super().__init__()
        self.options = webdriver.FirefoxOptions()
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=self.options)
        if headless:
            self.options.add_argument("--headless")
