
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators import HomePageLocators

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_icon = self.page.locator(HomePageLocators.LOGIN_ICON)

    def click_login_icon(self):
        self.click_element(self.login_icon)
























'''

'"""
home_page.py — represents the iTea home page.
All locators and actions for this page live here.
"""

import hashlib
import os
import requests
import urllib3

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

REFERENCE_DIR  = "reference_images"
REFERENCE_HASH = "reference_images/logo_hash.txt"



#Locators ────────────────────────────────────────────────────────────

class HomePageLocators:
    LOGO_WRAPPER = (By.CSS_SELECTOR, '#site-logo-inner')
    LOGO_IMG = (By.CSS_SELECTOR, '#site-logo-inner img')

#Actions ─────────────────────────────────────────────────────────────

class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def get_logo_element(self):
        return self.find_element(HomePageLocators.LOGO_WRAPPER)

    def get_logo_img(self):
        return self.find_element(HomePageLocators.LOGO_IMG)

    def is_logo_visible(self) -> bool:
        return self.is_element_visible(HomePageLocators.LOGO_WRAPPER)

    def get_logo_alt(self) -> str:
        return self.get_logo_img().get_attribute("alt")

    def get_logo_src(self) -> str:
        return self.get_logo_img().get_attribute("src")

    def compute_logo_md5(self) -> str:
        """Downloads the logo image and returns its MD5 fingerprint."""
        src = self.get_logo_src()
        response = requests.get(src, timeout=10, verify=False)  # verify=False skips SSL check
        response.raise_for_status()
        return hashlib.md5(response.content).hexdigest()

    def save_reference_hash(self, hash_value: str):
        os.makedirs(REFERENCE_DIR, exist_ok=True)
        with open(REFERENCE_HASH, "w") as f:
            f.write(hash_value)

    def load_reference_hash(self) -> str:
        with open(REFERENCE_HASH, "r") as f:
            return f.read().strip()

    def reference_hash_exists(self) -> bool:
        return os.path.exists(REFERENCE_HASH)
'''