from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bot"
    login: str = ""
    psw: str = ""
    browser: str = "chrome"
    headless: bool = True
    url_base: str = ""
    course_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
