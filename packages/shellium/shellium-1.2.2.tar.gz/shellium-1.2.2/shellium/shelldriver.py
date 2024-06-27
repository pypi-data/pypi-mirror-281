import time
from pathlib import Path
from shutil import rmtree
from subprocess import Popen, PIPE

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from .service import Service
from .options import Options
from .exceptions import *


class ShellElement(WebElement):
    def __init__(self, parent, _id):
        super().__init__(parent, _id)

    def find_element(self, by=By.ID, value=None) -> 'ShellElement':
        item = super().find_element(by, value)
        return ShellElement(item.parent, item.id)

    def find_elements(self, by=By.ID, value=None) -> list['ShellElement']:
        items = super().find_elements(by, value)
        return [ShellElement(item.parent, item.id) for item in items]

    def click(self, timeout=0.0,
              interval=0.1, ignore_errors=False):
        start = time.time()
        current_exception = WebDriverException
        while time.time() - start <= timeout:
            try:
                return super().click()
            except WebDriverException as exception:
                current_exception = exception
                time.sleep(interval)
        if ignore_errors:
            return None
        raise current_exception

    def check_element(self, by=By.ID, value=None,
                      interval=0.1, timeout=0.0):
        start = time.time()
        while time.time() - start <= timeout:
            try:
                return self.find_element(by, value)
            except WebDriverException:
                time.sleep(interval)
        return None

    def check_elements(self, by=By.ID, value=None,
                       interval=0.1, timeout=0.0):
        start_time = time.time()
        while time.time() - start_time <= timeout:
            items = self.find_elements(by, value)
            if items:
                return items
            time.sleep(interval)
        return None

    def send_keys(self, values, timeout=0.25):
        interval = timeout / len(values)
        for value in values:
            super().send_keys(value)
            time.sleep(interval)

    def is_exists(self):
        try:
            return self.is_displayed()
        except WebDriverException:
            return False


class ShellDriver(webdriver.Chrome):
    def __init__(self, options: Options = None, service: Service = None):
        super().__init__(options=options, service=service)

    def _wrap_value(self, value):
        if isinstance(value, ShellElement):
            return {"element-6066-11e4-a52e-4f735466cecf": value.id}
        return super()._wrap_value(value)

    def _unwrap_value(self, value):
        if isinstance(value, dict) and "element-6066-11e4-a52e-4f735466cecf" in value:
            return ShellElement(self, (value["element-6066-11e4-a52e-4f735466cecf"]))
        return super()._unwrap_value(value)

    def find_element(self, by=By.ID, value=None) -> ShellElement:
        item = super().find_element(by, value)
        return ShellElement(item.parent, item.id)

    def find_elements(self, by=By.ID, value=None) -> list[ShellElement]:
        items = super().find_elements(by, value)
        return [ShellElement(item.parent, item.id) for item in items]

    def check_element(self, by=By.ID, value=None,
                      interval=0.1, timeout=0.0):
        start = time.time()
        while time.time() - start <= timeout:
            try:
                return self.find_element(by, value)
            except WebDriverException:
                time.sleep(interval)
        return None

    def check_elements(self, by=By.ID, value=None,
                       interval=0.1, timeout=0.0):
        start_time = time.time()
        while time.time() - start_time <= timeout:
            items = self.find_elements(by, value)
            if items:
                return items
            time.sleep(interval)
        return None

    def scroll_into_view(self, item):
        if not isinstance(item, ShellElement):
            raise TypeError('Item Must be a ShellElement.')
        script = 'arguments[0].scrollIntoView({block: "center"});'
        return self.execute_script(script, item)


class Shellium:
    def __init__(self, executable_path=None,
                 user_data_dir=None, binary_location=None):
        # Setup options and service
        self._driver: ShellDriver | None = None
        self._options = Options()
        self._service = Service()

        # Setup paths
        if user_data_dir:
            self.options.user_data_dir = \
                user_data_dir
        if binary_location:
            self.options.binary_location = \
                binary_location
        if executable_path:
            self.service.path = \
                executable_path

    @property
    def driver(self):
        return self._driver

    @property
    def options(self):
        return self._options

    @property
    def service(self):
        return self._service

    def run(self) -> ShellDriver:
        if self.driver:
            raise ShellDriverAlreadyRunningError(f'The ShellDriver is already running: {self.driver}.')
        self._driver = ShellDriver(self.options, self.service)
        cmd = "Page.addScriptToEvaluateOnNewDocument"
        args = {'source': "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;"
                          "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;"
                          "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;"
                          "const newProto = navigator.__proto__;"
                          "delete newProto.webdriver;"
                          "navigator.__proto__ = newProto;"}
        self.driver.execute_cdp_cmd(cmd, args)
        return self.driver

    def terminate(self):
        if not self.driver:
            return None
        self.driver.quit()
        self._driver = None

    def build(self):
        if Path(self.options.user_data_dir).exists():
            raise UserDataDirExistsError(f'{self.options.user_data_dir} already exists.')

        process = Popen([self.options.binary_location, '--no-startup-window',
                         f'--user-data-dir={self.options.user_data_dir}'], stdout=PIPE)
        _, error = process.communicate()
        if process.returncode != 0:
            raise UserDataBuildError('Failed to build a User Data Dir.')

    def destroy(self):
        self.terminate()
        rmtree(self.options.user_data_dir, ignore_errors=True)
