from src.infra.browser.SeleniumBrowser import SeleniumBrowser
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium import webdriver


class Edge(SeleniumBrowser):
    """
    Edge browser class to create a Edge browser instance
    extends Browser class
    """

    def __init__(self, headless=False):
        super().__init__()
        self.options = webdriver.EdgeOptions()
        service = EdgeService(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=service, options=self.options)
        if headless:
            self.options.add_argument("--headless")
