
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators import HomePageLocators
import hashlib
import os
import re



class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_icon = self.page.locator(HomePageLocators.LOGIN_ICON)
        self.logo = self.page.locator(HomePageLocators.LOGO_IMAGE)

    def click_login_icon(self):
        self.click_element(self.login_icon)

    def is_logo_visible(self) -> bool:
        return self.logo.is_visible()

    def get_logo_alt(self) -> str:
        return self.logo.get_attribute("alt")

    def get_logo_src(self) -> str:
        return self.logo.get_attribute("src")

    def compute_logo_md5(self) -> str:
        image_url = self.get_logo_src()
        #visual testing trick to ensure the image hasn't silently changed or broken
        response = self.page.request.get(image_url, ignore_https_errors=True)  #downloads image with playwrights APIRequestContext avoiding SSL certificate
        image_bytes = response.body()
        return hashlib.md5(image_bytes).hexdigest()
        #compute_logo_md5: Downloads the image and uses the Python hashlib library to turn the image into a string like f3e5b7a....
        # save_reference_hash: The very first time you run the test, it creates a text file inside reference_images/ and saves that string.
        # load_reference_hash: On all future test runs, it reads that text file and compares it to the live website to make sure the logo is still exactly the same!

    def get_reference_path(self) -> str:
        #reates a folder called 'reference_images' if it doesn't exist
        os.makedirs("reference_images", exist_ok=True)
        return "reference_images/logo_hash.txt"

    def reference_hash_exists(self) -> bool:
        return os.path.exists(self.get_reference_path())

    def save_reference_hash(self, current_hash: str):
        with open(self.get_reference_path(), "w") as file:
            file.write(current_hash)

    def load_reference_hash(self) -> str:
        with open(self.get_reference_path(), "r") as file:
            return file.read().strip()

    def click_tea_menu(self):
        self.click_element(self.page.locator(HomePageLocators.TEA_MENU))

    def click_wishlist_icon(self):
        self.click_element(self.page.locator(HomePageLocators.WISHLIST))

    def click_cart_icon(self):
        self.click_element(self.page.locator(HomePageLocators.CART_ICON))

    def get_cart_item_count(self) -> int:
        count_locator = self.page.locator('span.count-item')
        self.page.wait_for_timeout(1000)
        return int(count_locator.inner_text()) #Get the text (e.g., "2") and convert it to an integer

    def click_wishlist_icon_visible(self):
        # Use the CSS visible one so it doesn't click hidden mobile menus
        self.click_element(self.page.locator(HomePageLocators.WISHLIST_VISIBLE))

    def click_cart_icon_visible(self):
        self.click_element(self.page.locator(HomePageLocators.CART_ICON_VISIBLE))

    def extract_price(self, price_text: str) -> float:
        """Extracts the active price from a WooCommerce string."""
        matches = re.findall(r'\d+\.?\d*', price_text)
        if matches:
            return float(matches[-1])
        return 0.0

    def get_amount_left_for_free_shipping(self) -> float:
        """Reads the header tracker and returns the exact math float."""

        # ADD .first SO PLAYWRIGHT DOESN'T CRASH IF IT FINDS MULTIPLE!
        tracker = self.page.locator('.oceanwp-woo-left-to-free').first

        if not tracker.is_visible():
            return 0.0  # If it's missing, we either hit the threshold or the UI is broken!

        text = tracker.inner_text()
        return self.extract_price(text)


















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