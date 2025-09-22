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
    browser.go_to(settings.url_base + settings.course_url)
    browser.click_button(xpaths.first_lesson_button)
    while True:
        while True:
            info("Verifying lesson status")
            if not browser.check_class_status():
                break
            info("Lesson completed")
            browser.next_lesson()
            sleep(1)
        if not browser.check_class_status():
            browser.play_video()
