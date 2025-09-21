from src.domain.model.Browser import Browser
from src.infra.browser import Chrome, Edge, Firefox


class BrowserFactory:
    @staticmethod
    def create_browser(browser: str) -> Browser:
        browsers: dict[str, type[Browser]] = {
            "chrome": Chrome,
            "firefox": Firefox,
            "edge": Edge,
        }

        _browser: type[Browser] | None = browsers.get(browser.lower())
        if _browser is None:
            raise ValueError(f"Unsupported browser: {browser}")

        return _browser()
