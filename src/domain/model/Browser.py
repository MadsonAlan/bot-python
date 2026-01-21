from abc import abstractmethod


class Browser:
    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Browser, cls).__new__(cls)
        return cls._instance

    @abstractmethod
    def launch(self) -> None:
        """Function to launch the browser instance"""
        pass

    @abstractmethod
    def go_to(self, url_site: str) -> None:
        """Function to navigate to a specific URL

        Args:
            url_site (str): url to navigate
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Function to close the browser instance"""
        pass

    @abstractmethod
    def fill_fild(self, campo: str, valor: str) -> None:
        """Function to fill a field in a web application

        Args:
            campo (str): field to be filled
            valor (str): value to fill the field
        """
        pass

    @abstractmethod
    def click_button(self, button: str) -> None:
        """Function to click a button in a web application

        Args:
            button (str): button to be clicked
        """
        pass

    @abstractmethod
    def check_class_status(self) -> bool:
        """Function to check the status of a class in a web application"""
        pass

    @abstractmethod
    def skip_video(self):
        """skip the lesson video"""
        pass

    @abstractmethod
    def next_lesson(self):
        """Navigate to the next lesson"""
        pass

    @abstractmethod
    def skip(self) -> None:
        """Press a key

        Args:
            string (str): key to press
        """
        pass

    @abstractmethod
    def log_page_header(self) -> None:
        """Log current page header/title"""
        pass
    @abstractmethod
    def save_last_url(self) -> None:
        """Save the last URL visited"""
        pass
    @abstractmethod
    def load_last_url(self) -> str:
        """Load the last URL visited"""
        pass
    @abstractmethod
    def get_current_lesson_duration(self) -> str:
        """Load the duration of the current lesson"""
        pass
    @abstractmethod
    def duration_to_seconds(self, text: str) -> int:
        """Convert duration text to seconds

        Args:
            text (str): duration text (e.g., "5m 30s")

        Returns:
            int: duration in seconds
        """
        pass

    @abstractmethod
    def play_video(self):
        """play the lesson video"""
        pass
