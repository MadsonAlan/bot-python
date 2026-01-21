from logging import error, info, warning
import random
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
    if browser.load_last_url() == settings.url_base+settings.course_url:
        browser.click_button(xpaths.first_lesson_button)
    MAX_LESSON_ATTEMPTS = 2
    MAX_STATUS_CHECKS = 12  
    while True:
        browser.save_last_url()

        lesson_attempts = 0
        lesson_completed = False

        while lesson_attempts < MAX_LESSON_ATTEMPTS and not lesson_completed:
            lesson_attempts += 1
            info("Lesson attempt %d/%d", lesson_attempts, MAX_LESSON_ATTEMPTS)

            if not browser.check_class_status():

                if browser.get_current_lesson_duration() == "0m 0s":
                    browser.skip_video()

                info("Duration found: %s", browser.get_current_lesson_duration())
                browser.play_video()

                seconds = (
                    browser.duration_to_seconds(
                        browser.get_current_lesson_duration()
                    ) + random.randint(5, 60)
                )

                minutes, secs = divmod(seconds, 60)
                info("Watching lesson for %02d:%02d", minutes, secs)
                sleep(seconds)

            # 🔎 Loop de verificação de conclusão
            status_checks = 0

            while status_checks < MAX_STATUS_CHECKS:
                browser.log_page_header()
                info("Verifying lesson status (%d/%d)", status_checks + 1, MAX_STATUS_CHECKS)

                if browser.check_class_status():
                    info("Lesson completed successfully")
                    lesson_completed = True
                    seconds_for_next=random.randint(5, 10)
                    info("Wait for %02ds", seconds_for_next)
                    sleep(seconds_for_next)
                    browser.next_lesson()
                    break

                status_checks += 1
                browser.skip()
                seconds_for_next_tentative=random.randint(5, 10)
                info("Wait for new tentative %02ds", seconds_for_next_tentative)
                sleep(seconds_for_next_tentative)

            if lesson_completed:
                break

            info("Lesson not completed after attempt %d", lesson_attempts)
            warning("Lesson not completed after attempt %d", lesson_attempts)

        if not lesson_completed:
            info("Lesson failed after %d attempts. Stopping execution.", MAX_LESSON_ATTEMPTS)
            error("Lesson failed after %d attempts. Stopping execution.", MAX_LESSON_ATTEMPTS)
            break

        sleep(5)
