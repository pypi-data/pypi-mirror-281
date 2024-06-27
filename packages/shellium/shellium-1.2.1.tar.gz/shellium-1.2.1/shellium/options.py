from selenium.webdriver.chrome import options
from pathlib import Path


class Options(options.Options):
    USER_DATA_DIR_ERROR = "User Data Dir Must be a String or a Path"
    BINARY_LOCATION_ERROR = "Binary Location Must be a String or a Path"

    def __init__(self):
        super().__init__()
        # Setup path to chrome.exe
        self._binary_location = Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
        self._user_data_dir = Path.home() / 'AppData/Local/Google/Chrome/User Data'
        self.add_argument(f"--user-data-dir={self.user_data_dir}")

        # Common options
        self.add_argument("--start-maximized")
        self.add_argument("–-disable-translate")
        self.add_argument("–disable-plugins")
        self.add_argument("--disable-extensions")

        # Setup undetected options
        self.add_argument("--disable-blink-features=AutomationControlled")
        self.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.add_experimental_option('useAutomationExtension', False)

    @property
    def user_data_dir(self) -> str:
        return str(self._user_data_dir)

    @property
    def binary_location(self):
        return str(self._binary_location)

    @property
    def headless(self):
        return '--headless' in self.arguments

    @binary_location.setter
    def binary_location(self, value):
        if not isinstance(value, (str, Path)):
            raise TypeError(self.BINARY_LOCATION_ERROR)
        self._binary_location = Path(value).resolve()

    @user_data_dir.setter
    def user_data_dir(self, value):
        if not isinstance(value, (str, Path)):
            raise TypeError(self.USER_DATA_DIR_ERROR)
        self._user_data_dir = Path(value).resolve()
        self._arguments = [item for item in self.arguments
                           if '--user-data-dir=' not in item]
        self.add_argument(f"--user-data-dir={self.user_data_dir}")

    @headless.setter
    def headless(self, value):
        if not isinstance(value, bool):
            raise TypeError('Headless Must be a bool.')
        if value and not self.headless:
            self.add_argument('--headless')
        if self.headless and not value:
            self._arguments.remove('--headless')

    def __repr__(self):
        return f"<Options at 0x{id(self)}: {self.arguments}>"
