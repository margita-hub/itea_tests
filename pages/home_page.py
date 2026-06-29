from playwright.sync_api import Page
from config.config import URL_EN
from pages.base_page import BasePage
from pages.locators import HomePageLocators
import hashlib
import os
import allure


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_icon = self.page.locator(HomePageLocators.LOGIN_ICON)
        self.logo = self.page.locator(HomePageLocators.LOGO_IMAGE)

    @allure.step("Load home page")
    def load(self):
        self.navigate_to(URL_EN)


    @allure.step("Click logo to go home")
    def click_logo(self):
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(300)
        self.logo.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Check logo is visible")
    def is_logo_visible(self) -> bool:
        return self.logo.is_visible()

    @allure.step("Get logo alt text")
    def get_logo_alt(self) -> str:
        return self.logo.get_attribute("alt")

    @allure.step("Get logo src")
    def get_logo_src(self) -> str:
        return self.logo.get_attribute("src")

    @allure.step("Compute logo MD5 hash")
    def compute_logo_md5(self) -> str:
        image_url = self.get_logo_src()
        response = self.page.request.get(image_url, ignore_https_errors=True)
        image_bytes = response.body()
        return hashlib.md5(image_bytes).hexdigest()

    def get_reference_path(self) -> str:
        os.makedirs("reference_images", exist_ok=True)
        return "reference_images/logo_hash.txt"

    def reference_hash_exists(self) -> bool:
        return os.path.exists(self.get_reference_path())

    @allure.step("Save reference hash")
    def save_reference_hash(self, current_hash: str):
        with open(self.get_reference_path(), "w") as file:
            file.write(current_hash)

    @allure.step("Load reference hash")
    def load_reference_hash(self) -> str:
        with open(self.get_reference_path(), "r") as file:
            return file.read().strip()



    @allure.step("Click login icon")
    def click_login_icon(self):
        self.click_element(self.login_icon)

    @allure.step("Click wishlist icon")
    def click_wishlist_icon(self):
        self.click_element(self.page.locator(HomePageLocators.WISHLIST))

    @allure.step("Click cart icon")
    def click_cart_icon(self):
        self.click_element(self.page.locator(HomePageLocators.CART_ICON))

    @allure.step("Click visible wishlist icon")
    def click_wishlist_icon_visible(self):
        self.click_element(self.page.locator(HomePageLocators.WISHLIST_VISIBLE))

    @allure.step("Click visible cart icon")
    def click_cart_icon_visible(self):
        self.click_element(self.page.locator(HomePageLocators.CART_ICON_VISIBLE))

    @allure.step("Get cart item count")
    def get_cart_item_count(self) -> int:
        count_locator = self.page.locator('span.count-item')
        self.page.wait_for_timeout(1000)
        return int(count_locator.inner_text())

    @allure.step("Get amount left for free shipping")
    def get_amount_left_for_free_shipping(self) -> float:
        tracker = self.page.locator('.oceanwp-woo-left-to-free').first
        if not tracker.is_visible():
            return 0.0
        text = tracker.inner_text()
        return self.extract_price(text)



    @allure.step("Click menu: {locator_name}")
    def click_menu(self, locator_name: str):
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(300)
        locator_string = getattr(HomePageLocators, locator_name)
        menu_link = self.page.locator(locator_string).first
        assert menu_link.is_visible(), f"Menu link '{locator_name}' not visible"
        menu_link.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Click Tea menu")
    def click_tea_menu(self):
        self.click_menu("TEA_MENU")

    @allure.step("Click Teaware menu")
    def click_teaware_menu(self):
        self.click_menu("TEAWARE_MENU")

    @allure.step("Click Coffee menu")
    def click_coffee_menu(self):
        self.click_menu("COFFEE_MENU")

    @allure.step("Click Sale menu")
    def click_sale_menu(self):
        self.click_menu("SALE_MENU")


    @allure.step("Hover Tea Types menu")
    def hover_tea_types_menu(self):
        self.page.locator('text="Tea Types"').first.hover(force=True)
        self.page.locator(HomePageLocators.MATCHA_MENU).first.wait_for(
            state="visible", timeout=5000
        )

    @allure.step("Hover submenu item: {item_text}")
    def hover_submenu_item(self, item_text: str):
        item_li = self.page.locator(f'li:has(a:has-text("{item_text}"))').first
        item_li.hover(force=True)
        self.page.wait_for_timeout(300)

    @allure.step("Get submenu item background color: {item_text}")
    def get_submenu_item_bg_color(self, item_text: str) -> str:
        item_li = self.page.locator(f'li:has(a:has-text("{item_text}"))').first
        return item_li.evaluate('el => window.getComputedStyle(el).backgroundColor')

    @allure.step("Check submenu item highlighted: {item_text}")
    def is_submenu_item_highlighted(self, item_text: str) -> bool:
        self.hover_submenu_item(item_text)
        bg_color = self.get_submenu_item_bg_color(item_text)
        return bg_color != "rgba(0, 0, 0, 0)"


    @allure.step("Get page heading")
    def get_page_heading(self) -> str:
        return self.page.locator('h1').first.inner_text().strip().lower()

    @allure.step("Check products missing sale badge")
    def products_missing_sale_badge(self) -> list:
        products = self.page.locator('li.product')
        products.first.wait_for(state="visible", timeout=5000)
        total = products.count()
        missing = []
        for i in range(total):
            if not products.nth(i).locator('.onsale').is_visible():
                missing.append(i)
        return missing

    @allure.step("Check products not containing: {keyword}")
    def products_not_containing(self, keyword: str) -> list:
        titles = self.page.locator('li.title.desktop a')
        titles.first.wait_for(state="visible", timeout=5000)
        total = titles.count()
        bad = []
        for i in range(total):
            title = titles.nth(i).inner_text().strip().lower()
            if keyword.lower() not in title:
                bad.append(title)
        return bad

    @allure.step("Close cart bounce popup")
    def close_cart_bounce_popup(self):
        try:
            popup = self.page.locator('.cart-bounce-close')
            if popup.is_visible():
                popup.click()
        except Exception:
            pass