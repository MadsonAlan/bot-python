from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from logging import error, info

from src.domain.model.Browser import Browser
from src.pkg.settings import XpathSettings


def verify_browser_contains_driver(func):
    def decorator(*args, **kwargs):
        if args[0].driver is None:
            error(
                "Driver not initialized. Use BrowserFactory to create a browser instance."
            )
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
            element = self.driver.find_element(
                By.CLASS_NAME, self.xpaths.wait_to_complete
            )
            info(element)
            r = True if element else False
        except Exception as e:
            error(e)
            pass
        return r

    @verify_browser_contains_driver
    def close(self) -> None:
        self.driver.quit()

    @verify_browser_contains_driver
    def fill_fild(self, campo: str, valor: str) -> None:
        @wait_element_present(5)
        def execute(s: SeleniumBrowser, c: str, v: str):
            element = s.driver.find_element(By.XPATH, c)
            element.clear()
            element.send_keys(v)

        execute(self, campo, valor)

    @verify_browser_contains_driver
    def click_button(self, button: str, by: str | None = None) -> None:
        @wait_element_present(5)
        def execute(s: SeleniumBrowser, c: str):
            element = s.driver.find_element(by if by != None else By.XPATH, c)
            info("Clicking in %s", c)
            element.click()

        execute(self, button)

    @verify_browser_contains_driver
    def play_video(self):
        WebDriverWait(self.driver, timeout=60).until(
            lambda driver: driver.find_element(
                By.XPATH, self.xpaths.video
            ).is_displayed()
        )
        element = self.driver.find_element(By.CSS_SELECTOR, self.xpaths.video)
        self.driver.execute_script(
            "var iframe = arguments[0]; iframe.contentWindow.postMessage(JSON.stringify({method: 'play'}), '*');",
            element,
        )
        info(
            "Vídeo em execução: %s",
            not self.driver.execute_script("return arguments[0].paused;", element),
        )

    def next_lesson(self):
        info("Changing for the next lesson")
        self.click_button(self.xpaths.next_lesson_button)
