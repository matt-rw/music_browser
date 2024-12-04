"""Browser."""
import os
import requests
import threading
import math

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from requests.exceptions import ConnectionError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service


# TODO:
# - Add support for Chrome in addition to Firefox
# - Handle errors if not connected to the internet


"""Selenium Firefox browser.

May require valid github GH_TOKEN environment variable.
May need geckodriver binary.

"""
class BaseBrowser:
    def __init__(self, base_url: str, browser_type: str = 'Firefox'):
        """Init.

        Args:
            base_url (str)
            browser_type (str): one of 'Firefox' of 'Chrome'

        """
        self.base_url = base_url
        self.browser: Optional[Firefox]= None
        self.browser_t: Optional[Thread] = None

    def find_and_click(
        self, 
        element, 
        timeout: int = 3, 
        rounds: int = 2
    ) -> None:
        """Waits for element and clicks if found.
        
        element: button identifier
            (e.g. (By.CLASS_NAME, 'ytp-ad-skip-button-container'))
        timeout (int): seconds to wait for each round
        rounds (int): number of attempts to find element

        """
        for i in range(rounds):
            wait = WebDriverWait(self.browser, timeout)
            visible = EC.visibility_of_element_located(element)
            wait.until(visible)
            button = self.browser.find_element(element)
            button.click()

    def start(self, url: str, headless: bool = True) -> None:
        """Runs selenium in a thread optionally in headless mode.

        Args:
            url (str): 
            headless (bool): whether to not open a window, default True

        """
        gecko = GeckoDriverManager()
        try:
            gecko_path = gecko.install()
        except ConnectionError:
            return

        options = FirefoxOptions()
        service = Service(executable_path=gecko_path)
        if headless:
            options.add_argument('--headless')
        self.browser = Firefox(service=service, options=options)

        wait = WebDriverWait(self.browser, 5)
        # presence = EC.presence_of_element_located
        visible = EC.visibility_of_element_located

        self.browser.get(url)
        wait.until(visible((By.ID, 'primary-inner')))
        self.browser.find_element(By.ID,'primary-inner').click()

        S = threading.Timer(8.0, self.skip)
        S.start()

    def close(self) -> None:
        """Join browser thread."""
        self.browser.close()
        self.browser_t.join()
