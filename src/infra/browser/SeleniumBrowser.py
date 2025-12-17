import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging import error, info
from src.domain.model.Browser import Browser
from src.pkg.settings import XpathSettings, xpath_settings


def _verify_browser_contains_driver(func):
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


def _wait_element_present(timeout):
    def decorator(func):
        def wrapper(self, campo, *args, **kwargs):
            WebDriverWait(self.driver, timeout=timeout).until(
                lambda driver: driver.find_element(By.XPATH, campo).is_displayed()
            )
            return func(self, campo, *args, **kwargs)

        return wrapper

    return decorator


def _wait_element_clickable(timeout):
    def decorator(func):
        def wrapper(self, campo, *args, **kwargs):
            WebDriverWait(self.driver, timeout=timeout).until(
                EC.element_to_be_clickable((By.XPATH, campo))
            )
            return func(self, campo, *args, **kwargs)

        return wrapper

    return decorator

class SeleniumBrowser(Browser):
    driver: webdriver.Remote

    def __init__(self):
        self.driver = None
        self.xpaths = XpathSettings()

    @_verify_browser_contains_driver
    def launch(self):
        pass

    @_verify_browser_contains_driver
    def go_to(self, url: str) -> None:
        self.driver.get(url)

    @_verify_browser_contains_driver
    def check_class_status(self) -> bool:
        r = False
        try:
            element = self.driver.find_element(
                By.CLASS_NAME, self.xpaths.wait_to_complete
            )
            r = True if element.text.strip() else False
        except Exception as e:
            error(e)
            pass
        return r

    @_verify_browser_contains_driver
    def close(self) -> None:
        self.driver.switch_to.default_content()
        self.driver.quit()

    @_verify_browser_contains_driver
    def fill_fild(self, campo: str, valor: str) -> None:
        @_wait_element_present(5)
        def execute(s: SeleniumBrowser, c: str, v: str):
            element = s.driver.find_element(By.XPATH, c)
            element.clear()
            element.send_keys(v)

        execute(self, campo, valor)

    @_verify_browser_contains_driver
    def click_button(self, button: str, by: str | None = None, tryed: bool = False) -> None:
        @_wait_element_clickable(5)
        def execute(s: SeleniumBrowser, c: str, t: bool):
            try:
                element = s.driver.find_element(by if by != None else By.XPATH, c)
                info("Clicking in %s", c)
                element.click()
            except Exception as e:
                if not t:
                    self.click_button(xpath_settings.btn_close, By.XPATH, True)
                    time.sleep(1)
                    self.click_button(c, By.XPATH, True)

        execute(self, button, tryed)

    @_verify_browser_contains_driver
    def play_video(self):
        cookies = self.driver.get_cookies()
        csrf_token = self.driver.find_element(By.NAME, '_csrf').get_attribute('value')
        requests.post(f"{self.driver.current_url}/completion", cookies={cookie['name']: cookie['value'] for cookie in cookies}, headers={'X-CSRF-TOKEN': csrf_token})
        self.driver.refresh()
        info("Video played")

    def next_lesson(self):
        info("Changing for the next lesson")
        self.click_button(self.xpaths.next_lesson_button)

    @_verify_browser_contains_driver
    def skip(self) -> None:
        element = self.driver.find_element(By.CSS_SELECTOR, self.xpaths.video)
        element.send_keys(Keys.ARROW_RIGHT)
