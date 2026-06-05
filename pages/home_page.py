
from playwright.sync_api import Page
from config.config import URL_EN
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

    def load(self):
        self.navigate_to(URL_EN)

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



    def get_amount_left_for_free_shipping(self) -> float:
        #takes the header tracker and returns the exact math float.
        # ADD .first SO PLAYWRIGHT DOESN'T CRASH IF IT FINDS MULTIPLE!
        tracker = self.page.locator('.oceanwp-woo-left-to-free').first

        if not tracker.is_visible():
            return 0.0  # If it's missing, we either hit the threshold or the UI is broken!
        text = tracker.inner_text()
        return self.extract_price(text)

    def hover_tea_types_menu(self):
        self.page.locator('text="Tea Types"').first.hover(force=True)
        self.page.wait_for_timeout(800)   # wait for dropdown animation

    def click_menu(self, locator_name: str):
        locator_string = getattr(HomePageLocators, locator_name)
        menu_link = self.page.locator(locator_string).first
        assert menu_link.is_visible(), f"Menu link '{locator_name}' not visible in header"
        menu_link.click()


    def all_products_have_sale_badge(self) -> bool:
        products = self.page.locator('li.product')
        products.first.wait_for(state="visible", timeout=5000)
        total = products.count()
        assert total > 0, "No products found on Sale page"
        for i in range(total):
            if not products.nth(i).locator('.onsale').is_visible():
                return False
        return True

    def all_product_titles_contain(self, keyword: str) -> bool:
        titles = self.page.locator('li.title.desktop a')
        titles.first.wait_for(state="visible", timeout=5000)
        total = titles.count()
        assert total > 0, "No product titles found on page"
        for i in range(total):
            if keyword.lower() not in titles.nth(i).inner_text().strip().lower():
                return False
        return True

    def hover_tea_types_menu(self):
        self.page.locator('text="Tea Types"').first.hover(force=True)
        self.page.locator(HomePageLocators.MATCHA_MENU).first.wait_for(
            state="visible", timeout=5000
        )

    def click_menu(self, locator_name: str):
        locator_string = getattr(HomePageLocators, locator_name)
        menu_link = self.page.locator(locator_string).first
        assert menu_link.is_visible(), f"Menu link '{locator_name}' not visible in header"
        menu_link.click()
