import sys

from src.infra.browser.BrowserFactory import BrowserFactory
from src.infra.browser.SeleniumBrowser import SeleniumBrowser

if __name__ == "__main__":
    if len(sys.argv) > 1:
        browser_name = sys.argv[1]
        browser = BrowserFactory.create_browser(browser_name)
    else:
        browser = SeleniumBrowser()
    browser.launch()
    print("Browser launched successfully!")
    browser.close()
