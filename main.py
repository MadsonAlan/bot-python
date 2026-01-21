from logging import error

from src.infra.browser.BrowserFactory import BrowserFactory
from src.domain.usecases import abrir_curso
from src.pkg.settings import settings, xpath_settings
from logging import WARNING, DEBUG, INFO
from logging import basicConfig
from logging import FileHandler, StreamHandler


file_handler = FileHandler("logs.log", "a")
file_handler.setLevel(WARNING)


stream_handler = StreamHandler()

basicConfig(
    level=INFO,
    format="%(levelname)s: %(asctime)s -> %(message)s",
    handlers=[file_handler, stream_handler],
)
if __name__ == "__main__":
    browser_name = settings.browser

    browser = BrowserFactory.create_browser(browser_name, headless=settings.headless)
    try:
        abrir_curso(browser, settings, xpath_settings)
    except Exception as e:
        error(e)
        pass
    finally:
        browser.close()
        pass
