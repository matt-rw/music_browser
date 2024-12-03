"""Browser."""
import os
import requests
import threading
import math

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service

from browser.base_browser import BaseBrowser

"""Selenium Firefox browser.

May require valid github GH_TOKEN environment variable.
May need geckodriver binary.

"""
class YouTubeBrowser(BaseBrowser):
    def __init__(self, base_url: str='https://youtube.com'):
        # self.base_url = base_url
        super().__init__(base_url)

    def read_input(self, *args) -> str:
        """Formats URL with arguments"""
        # TODO: replace args with SearchConfig
        url = f'{self.base_url}/results?search_query='
        for arg in args:
            url += f'{arg.replace(" ", "+")}+'
        return url
    
    def skip(self) -> None:
        """Attempts to skip a Youtube add."""
        try:
            for i in range(2):
                wait = WebDriverWait(self.browser, 6)
                visible = EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'ytp-ad-skip-button-container')
                )
                wait.until(visible)
                skip_button = self.browser.find_element(
                    By.CLASS_NAME,
                    'ytp-ad-skip-button-container'
                )
                skip_button.click()
        except:
            pass

    def retrieve_links(self, url): 
        """Finds Youtube links for the given url."""
        # TODO: replace selenium with requests.get(url)
        options = FirefoxOptions()
        options.add_argument('--headless')
        service = Service(
            executable_path=GeckoDriverManager().install()
        )
        self.browser = Firefox(service=service, options=options)
        wait = WebDriverWait(self.browser, 5)
        presence = EC.presence_of_element_located
        visible = EC.visibility_of_element_located((By.ID, 'logo-icon'))
        self.browser.get(url)
        wait.until(visible)
        source = self.browser.page_source

        # source = requests.get(url)
        soup = BeautifulSoup(source, 'html.parser')

        # TODO: return page source
        links = soup.find_all(
            'a',
            {'class':'yt-simple-endpoint style-scope ytd-video-renderer'}, 
            href=True
        )
        
        new_links = []
        for link in links:
            new_links.append((link['title'],link['href']))
        
        self.browser.quit()
        return new_links 
    
    def show_link(self, url: str, show: bool) -> None:
        """Opens a selenium in a thread."""
        # TODO: replace URL with full URL
        url = 'https://www.youtube.com' + url
    
        options = FirefoxOptions()
        if show:
            options = FirefoxOptions()
            service = Service(
                executable_path=GeckoDriverManager().install()
            )
            self.browser = Firefox(service=service, options=options)
        else:
            options.add_argument('--headless')
            service = Service(
                executable_path=GeckoDriverManager().install()
            )
            self.browser = Firefox(service=service, options=options)

        wait = WebDriverWait(self.browser, 5)
        # presence = EC.presence_of_element_located
        visible = EC.visibility_of_element_located

        self.browser.get(url)
        wait.until(visible((By.ID, 'primary-inner')))
        self.browser.find_element(By.ID,'primary-inner').click()

        S = threading.Timer(8.0, self.skip)
        S.start()
