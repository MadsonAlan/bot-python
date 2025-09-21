from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from src.domain.model.Browser import Browser
from src.pkg.settings import XpathSettings


def verify_browser_contains_driver(func):
    def decorator(self, *args, **kwargs):
        if self.driver is None:
            raise Exception(
                "Driver not initialized. Use BrowserFactory to create a browser instance."
            )
        return func(*args, **kwargs)

    return decorator


def wait_element_present(timeout):
    def decorator(func):
        def wrapper(self, campo, *args, **kwargs):
            WebDriverWait(self.driver, timeout=timeout).until(
                lambda driver: driver.find_element(By.XPATH, campo).is_displayed()
            )
            return func(self, campo, *args, **kwargs)

        return wrapper

    return decorator


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
        r = False
        try:
            element = self.driver.find_element(By.XPATH, self.xpaths.wait_to_complete)
            r = True if element else False
        except:
            pass
        return r

    @verify_browser_contains_driver
    def close(self) -> None:
        self.driver.quit()

    @wait_element_present(60)
    @verify_browser_contains_driver
    def fill_fild(self, campo: str, valor: str) -> None:
        element = self.driver.find_element(By.XPATH, campo)
        element.clear()
        element.send_keys(valor)

    @wait_element_present(60)
    @verify_browser_contains_driver
    def click_button(self, button: str) -> None:
        element = self.driver.find_element(By.XPATH, button)
        element.click()
