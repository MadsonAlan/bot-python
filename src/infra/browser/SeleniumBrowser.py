from selenium import webdriver

from src.domain.model.Browser import Browser
from src.pkg.settings import XpathSettings


def verify_browser_contains_driver(func):
    def inner(*args, **kwargs):
        if args[0].driver is None:
            raise Exception(
                "Driver not initialized. Use BrowserFactory to create a browser instance."
            )
        return func(*args, **kwargs)

    return inner


class SeleniumBrowser(Browser):
    driver: webdriver.Remote

    def __init__(self):
        self.driver = None
        self.xpaths = XpathSettings()

    @verify_browser_contains_driver
    def launch(self):
        pass

    @verify_browser_contains_driver
    def go_to(self, url: str) -> None:
        self.driver.get(url)

    @verify_browser_contains_driver
    def check_class_status(self) -> bool:
        try:
            element = self.driver.find_element("xpath", self.xpaths.wait_to_complete)
            return True if element else False
        except Exception:
            return False
        return False

    @verify_browser_contains_driver
    def close(self) -> None:
        self.driver.quit()

    @verify_browser_contains_driver
    def fill_fild(self, campo: str, valor: str) -> None:
        element = self.driver.find_element("xpath", campo)
        element.clear()
        element.send_keys(valor)

    @verify_browser_contains_driver
    def click_button(self, button: str) -> None:
        element = self.driver.find_element("xpath", button)
        element.click()
