from playwright.sync_api import Page
from config.config import URL_EN
from pages.base_page import BasePage
from pages.locators import HomePageLocators
import hashlib
import os


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_icon = self.page.locator(HomePageLocators.LOGIN_ICON)
        self.logo = self.page.locator(HomePageLocators.LOGO_IMAGE)

    def load(self):
        self.navigate_to(URL_EN)

    # ============================================================
    # LOGO
    # ============================================================

    def click_logo(self):
        """Click logo to go home."""
        self.logo.click()
        self.page.wait_for_load_state("domcontentloaded")

    def is_logo_visible(self) -> bool:
        return self.logo.is_visible()

    def get_logo_alt(self) -> str:
        return self.logo.get_attribute("alt")

    def get_logo_src(self) -> str:
        return self.logo.get_attribute("src")

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

    def save_reference_hash(self, current_hash: str):
        with open(self.get_reference_path(), "w") as file:
            file.write(current_hash)

    def load_reference_hash(self) -> str:
        with open(self.get_reference_path(), "r") as file:
            return file.read().strip()

    # ============================================================
    # NAVIGATION - HEADER ICONS
    # ============================================================

    def click_login_icon(self):
        self.click_element(self.login_icon)

    def click_wishlist_icon(self):
        self.click_element(self.page.locator(HomePageLocators.WISHLIST))

    def click_cart_icon(self):
        self.click_element(self.page.locator(HomePageLocators.CART_ICON))

    def click_wishlist_icon_visible(self):
        self.click_element(self.page.locator(HomePageLocators.WISHLIST_VISIBLE))

    def click_cart_icon_visible(self):
        self.click_element(self.page.locator(HomePageLocators.CART_ICON_VISIBLE))

    def get_cart_item_count(self) -> int:
        count_locator = self.page.locator('span.count-item')
        self.page.wait_for_timeout(1000)
        return int(count_locator.inner_text())

    def get_amount_left_for_free_shipping(self) -> float:
        tracker = self.page.locator('.oceanwp-woo-left-to-free').first
        if not tracker.is_visible():
            return 0.0
        text = tracker.inner_text()
        return self.extract_price(text)

    # ============================================================
    # NAVIGATION - MAIN MENU
    # ============================================================

    def click_menu(self, locator_name: str):
        """Click any main menu item by locator name."""
        locator_string = getattr(HomePageLocators, locator_name)
        menu_link = self.page.locator(locator_string).first
        assert menu_link.is_visible(), f"Menu link '{locator_name}' not visible"
        menu_link.click()
        self.page.wait_for_load_state("domcontentloaded")

    def click_tea_menu(self):
        self.click_menu("TEA_MENU")

    def click_teaware_menu(self):
        """Click Teaware in main menu."""
        self.click_menu("TEAWARE_MENU")

    def click_coffee_menu(self):
        """Click Coffee in main menu."""
        self.click_menu("COFFEE_MENU")

    def click_sale_menu(self):
        """Click Sale in main menu."""
        self.click_menu("SALE_MENU")

    # ============================================================
    # NAVIGATION - TEA TYPES SUBMENU
    # ============================================================

    def hover_tea_types_menu(self):
        """Hover over Tea Types to reveal submenu."""
        self.page.locator('text="Tea Types"').first.hover(force=True)
        self.page.locator(HomePageLocators.MATCHA_MENU).first.wait_for(
            state="visible", timeout=5000
        )

    def hover_submenu_item(self, item_text: str):
        """Hover over a submenu item."""
        item_li = self.page.locator(f'li:has(a:has-text("{item_text}"))').first
        item_li.hover(force=True)
        self.page.wait_for_timeout(300)

    def get_submenu_item_bg_color(self, item_text: str) -> str:
        item_li = self.page.locator(f'li:has(a:has-text("{item_text}"))').first
        return item_li.evaluate('el => window.getComputedStyle(el).backgroundColor')

    def is_submenu_item_highlighted(self, item_text: str) -> bool:
        self.hover_submenu_item(item_text)
        bg_color = self.get_submenu_item_bg_color(item_text)
        return bg_color != "rgba(0, 0, 0, 0)"

    # ============================================================
    # PAGE ASSERTIONS
    # ============================================================

    def get_page_heading(self) -> str:
        return self.page.locator('h1').first.inner_text().strip().lower()

    def products_missing_sale_badge(self) -> list:
        products = self.page.locator('li.product')
        products.first.wait_for(state="visible", timeout=5000)
        total = products.count()
        missing = []
        for i in range(total):
            if not products.nth(i).locator('.onsale').is_visible():
                missing.append(i)
        return missing

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

    def close_cart_bounce_popup(self):
        """Close popup if it appears."""
        try:
            popup = self.page.locator('.cart-bounce-close')
            if popup.is_visible():
                popup.click()
        except Exception:
            pass