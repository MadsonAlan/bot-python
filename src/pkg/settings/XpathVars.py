class XpathSettings:
    login_input: str = "/html/body/div[2]/form/div/div[2]/div[1]/input"
    psw_input: str = "/html/body/div[2]/form/div/div[2]/div[2]/input"
    login_button: str = "/html/body/div[2]/form/div/div[2]/div[3]/button"
    first_lesson_button: str = '//*[@id="tab-curriculum"]/ol/li[1]/ol/li[1]'
    wait_to_complete: str = "js-lesson-completed"
    next_lesson_button: str = (
        "//div[contains(@class, 'c-video-navigator--next')]/a[contains(@class, 'c-video-navigator__arrow')]"
    )
    complete_lesson_when_not_a_video: str = "/html/body/div[4]/div/div[1]/a"
    video: str = "iframe[src*='player.vimeo.com']"
    btn_close = '//*[@id="pdv4close"]'
