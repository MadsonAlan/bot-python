import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging import error, info
from src.domain.model.Browser import Browser
from src.pkg.settings import XpathSettings, xpath_settings, settings
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException
)
import logging
import time
from pathlib import Path
from urllib.parse import urlparse
import re

BASE_DIR = Path(__file__).resolve().parent
LAST_URL_FILE = BASE_DIR / "last_url.txt"
LAST_URL_FILE.touch(exist_ok=True)

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
    def accept_cookies_if_present(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                   (By.XPATH, "//button[contains(normalize-space(), 'OK')]")
                )
            )
            logging.info("Accepting cookies banner")
            btn.click()
        except Exception:
            pass

    @_verify_browser_contains_driver
    def click_button(self, button: str, by: str | None = None, retries: int = 1) -> None:
        locator = (by if by else By.XPATH, button)

        try:
            self.accept_cookies_if_present()
            logging.info("Clicking in %s", button)

            element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()

        except (StaleElementReferenceException,
                ElementClickInterceptedException,
                TimeoutException) as e:

            logging.warning("Click failed (%s). Retrying...", type(e).__name__)

            if retries > 0:
                # tenta fechar modal se existir
                try:
                    close_btn = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_settings.btn_close))
                    )
                    close_btn.click()
                    time.sleep(0.5)
                except Exception:
                    pass

                self.click_button(button, by, retries - 1)
            else:
                logging.exception("Click permanently failed")
                raise
    @_verify_browser_contains_driver
    def skip_video(self):
        cookies = self.driver.get_cookies()
        csrf_token = self.driver.find_element(By.NAME, '_csrf').get_attribute('value')
        requests.post(f"{self.driver.current_url}/completion", cookies={cookie['name']: cookie['value'] for cookie in cookies}, headers={'X-CSRF-TOKEN': csrf_token})
        self.driver.refresh()
        info("Video skiped")

    def next_lesson(self):
        info("Changing for the next lesson")
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, self.xpaths.next_lesson_button))
        )

        # garante que está visível
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(element)
        )
        self.click_button(self.xpaths.next_lesson_button)

    @_verify_browser_contains_driver
    def skip(self) -> None:
        element = self.driver.find_element(By.CSS_SELECTOR, self.xpaths.video)
        element.send_keys(Keys.ARROW_RIGHT)

    @_verify_browser_contains_driver
    def save_last_url(self) -> None:
        try:
            LAST_URL_FILE.write_text(self.driver.current_url, encoding="utf-8")
            logging.info("Saved last URL: %s", self.driver.current_url)
        except Exception as e:
            logging.error("Could not save last URL: %s", e)

    @_verify_browser_contains_driver
    def load_last_url(self) -> str:
        if LAST_URL_FILE.exists():
            url = LAST_URL_FILE.read_text(encoding="utf-8").strip()
            if url:
                logging.info("Loaded last URL: %s", url)
                return url
        return settings.url_base + settings.course_url
    
    @_verify_browser_contains_driver
    def get_current_lesson_duration(self) -> str:
        try:
            xpath = (
                "//a[contains(@class,'c-course-curriculum__lesson-container') "
                f"and @href='{urlparse(self.driver.current_url).path}']"
                "//span[contains(@class,'c-course-curriculum__lesson-duration')]"
            )
            span = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return span.text.strip() 

        except Exception:
            return "0m 0s"
    
    @_verify_browser_contains_driver
    def duration_to_seconds(self, text: str) -> int:
        minutes = re.search(r"(\d+)\s*m", text)
        seconds = re.search(r"(\d+)\s*s", text)

        total = 0
        if minutes:
            total += int(minutes.group(1)) * 60
        if seconds:
            total += int(seconds.group(1))

        return total
    @_verify_browser_contains_driver
    def play_video(self):
        driver = self.driver
        try:
            driver.execute_script("""
                const ids = ['pdv4overlay', 'cookie-banner', 'overlay', 'modal'];
                ids.forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.remove();
                });
            """)
            # 1️⃣ Entrar no iframe (qualquer player conhecido)
            WebDriverWait(driver, 15).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[src*='vdocipher'], iframe[src*='player']")
                )
            )

            # 2️⃣ Tentar botão Play por classes conhecidas
            play_selectors = [
                ".Button_module_button__61be5b9c",
                ".PlayNPause",
                ".overlay-play",
                "[aria-label='Play']"
            ]

            for selector in play_selectors:
                try:
                    play_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    play_button.click()
                    info("Play button clicked (%s)", selector)
                    return
                except TimeoutException:
                    continue

            # 3️⃣ Fallback: clicar no centro do player
            info("Play button not found, clicking center of player")

            driver.execute_script("""
                const video = document.querySelector('video');
                if (video) {
                    video.muted = true;
                    video.play();
                }
            """)
            is_playing = driver.execute_script("""
                const v = document.querySelector('video');
                return v && !v.paused;
            """)

            info("Rodando: %s", is_playing)

        except Exception as e:
            error("Failed to play video: %s", e)
            driver.switch_to.default_content()
            self.skip_video()

        finally:
            # 4️⃣ Sempre voltar ao contexto principal
            driver.switch_to.default_content()