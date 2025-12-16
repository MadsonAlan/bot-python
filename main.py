from logging import error

from src.infra.browser.BrowserFactory import BrowserFactory
from src.domain.usecases import abrir_curso
from src.pkg.settings import settings, xpath_settings

if __name__ == "__main__":
    browser_name = settings.browser

    browser = BrowserFactory.create_browser(browser_name, headless=settings.headless or True)
    try:
        abrir_curso(browser, settings, xpath_settings)
    except Exception as e:
        error(e)
        pass
    finally:
        browser.close()
        pass
