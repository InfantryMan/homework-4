# -*- coding: utf-8 -*-

import sys
import urlparse

from page import Page
from tests.components.sidebar import Sidebar
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage(Page):
    BASE_URL = 'https://octavius.mail.ru/'

    @property
    def sidebar(self):
        return Sidebar(self.driver)

    def redirectToQa(self):
        url = urlparse.urljoin(self.BASE_URL, '/bundles/page.qa.html')
        self.driver.get(url)
