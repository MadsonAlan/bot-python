from src.infra.browser.SeleniumBrowser import SeleniumBrowser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver


class Chrome(SeleniumBrowser):
    """
    Chrome browser class to create a Chrome browser instance
    extends Browser class
    """

    def __init__(self, headless=False):
        super().__init__()
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)
