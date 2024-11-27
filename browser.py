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


# TODO:
# - Abstract youtube out of class
# - Convert into instance methods
# - Add support for Chrome in addition to Firefox


"""Selenium Firefox browser.

May require valid github GH_TOKEN environment variable.

"""
class Browser:
    def readInput(self, args=None):
        if args==None:
            args = ['']*2
            args[0] = input('Artist name: ')
            args[1] = input('Song name: ').replace(' ', '+')
        args[0] = args[0].replace(' ', '+')
        args[1] = args[1].replace(' ', '+')
        url = f'https://www.youtube.com/results?search_query={args[0]}+{args[1]}'
        
        if args[2] == 1:
            url = url + '+[live]'
        
        return url
    
    def skip(self):
        try:
            for i in range(2):
                wait = WebDriverWait(self.browser, 6)
                visible = EC.visibility_of_element_located
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
        # options = FirefoxOptions()
        # options.add_argument('--headless')
        # service = Service(
        #    executable_path=GeckoDriverManager().install()
        # )
        # self.browser = Firefox(service=service, options=options)
        # wait = WebDriverWait(self.browser, 5)
        # presence = EC.presence_of_element_located
        # visible = EC.visibility_of_element_located((By.ID, 'logo-icon'))
        # self.browser.get(url)
        # wait.until(visible)
        # source = self.browser.page_source

        requests.get(url)
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
    
    def showLink(self, link: str, show: bool) -> None:
        """Opens a selenium in a thread and attempt to skip adds."""
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

        url = 'https://www.youtube.com' + link
    
        wait = WebDriverWait(self.browser, 5)
        # presence = EC.presence_of_element_located
        visible = EC.visibility_of_element_located

        self.browser.get(url)
        wait.until(visible((By.ID, 'primary-inner')))
        self.browser.find_element(By.ID,'primary-inner').click()

        S = threading.Timer(8.0, self.skip)
        S.start()
