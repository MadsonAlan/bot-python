from logging import info
from time import sleep

from src.domain.model import Browser
from src.pkg.settings import Settings, XpathSettings


def abrir_curso(browser: Browser, settings: Settings, xpaths: XpathSettings) -> None:
    from src.domain.usecases.realizar_login import realizar_login

    """Function to open a course page in a web application

    Args:
        browser (Browser): Browser instance
        course_url (str): URL of the course page
    """
    realizar_login(browser, settings, xpaths)
    browser.go_to(browser.load_last_url())
    browser.click_button(xpaths.first_lesson_button)
    while True:
        if not browser.check_class_status():
            browser.play_video()
        while True:
            browser.log_page_header()
            info("Verifying lesson status")
            if browser.check_class_status():
                info("Lesson completed")
                browser.save_last_url()
                browser.next_lesson()
                break
            else:
                browser.skip()
            sleep(5)
        sleep(5)
