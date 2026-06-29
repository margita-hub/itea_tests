import re
import allure
from playwright.sync_api import Page
from config.config import TEA_URL
from pages.base_page import BasePage
from pages.locators import TeaPageLocators


class TeaPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Load tea page")
    def load(self):
        self.navigate_to(TEA_URL)

    @allure.step("Check tea page loaded")
    def is_page_loaded(self) -> bool:
        title_locator = self.page.locator('h1.page-header-title')
        try:
            title_locator.wait_for(state="visible", timeout=5000)
            return "Tea" in title_locator.inner_text()
        except Exception:
            return False

    def get_product_at_index(self, index: int):
        return (
            self.page
            .locator(TeaPageLocators.PRODUCT_LIST)
            .locator(TeaPageLocators.PRODUCT_ITEM)
            .nth(index)
        )

    def get_product_title(self, product_element) -> str:
        return product_element.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()

    def get_product_price(self, product_element) -> float:
        price_text = product_element.locator('.price').inner_text()
        return self.extract_price(price_text)

    def get_expected_sale_count(self) -> int:
        return self.page.locator('li.product span.onsale').count()

    def has_sale_badge(self, product_element) -> bool:
        sale_badge = product_element.locator(TeaPageLocators.SALE_BADGE)  # ← add variable!
        return sale_badge.count() > 0 and sale_badge.is_visible()

    def get_sale_discount(self, product_element) -> int:
        sale_badge = product_element.locator(TeaPageLocators.SALE_BADGE)  # ← add variable!
        sale_text = sale_badge.inner_text().strip()
        match = re.search(r'\d+', sale_text)
        return int(match.group()) if match else 0

    @allure.step("Click Select Options button for product at index {index}")
    def click_select_options_button_for_product(self, index: int):
        product_list = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        select_options_products = product_list.locator(TeaPageLocators.SELECT_OPTIONS_PRODUCT_ITEM)
        product_item = select_options_products.nth(index)
        item_name = product_item.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()
        button = product_item.locator(TeaPageLocators.ADD_TO_CART_BTN)
        self.click_and_catch_false_toast(button, "Select options (list)")
        self.page.wait_for_load_state("domcontentloaded")
        return item_name

    @allure.step("Add item to wishlist by name: {tea_name}")
    def add_item_to_wishlist_by_name(self, tea_name: str) -> bool:
        product_list = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        specific_product = (
            product_list
            .locator(TeaPageLocators.PRODUCT_ITEM)
            .filter(has_text=tea_name)
            .first
        )
        wishlist_btn = specific_product.locator(TeaPageLocators.ADD_TO_WISHLIST_BTN)
        specific_product.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        box = wishlist_btn.bounding_box()
        if box:
            self.page.mouse.move(
                box["x"] + box["width"] / 2,
                box["y"] + box["height"] / 2,
                steps=10
            )
            self.page.wait_for_timeout(300)
            self.page.mouse.down()
            self.page.wait_for_timeout(150)
            self.page.mouse.up()
        else:
            wishlist_btn.click(delay=150)
        try:
            filled_heart = specific_product.locator(TeaPageLocators.WISHLIST_HEART_FILLED)
            filled_heart.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    @allure.step("Add item to wishlist via product page at index {index}")
    def add_item_to_wishlist_via_product_page(self, index: int) -> str | None:
        product_list = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        product_element = product_list.locator(TeaPageLocators.PRODUCT_ITEM).nth(index)
        item_name = product_element.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()
        title_locator = product_element.locator(TeaPageLocators.PRODUCT_TITLE)
        self.click_element(title_locator)
        self.page.wait_for_load_state("networkidle")
        wishlist_btn = self.page.locator(TeaPageLocators.SINGLE_PRODUCT_WISHLIST_BTN).first
        try:
            wishlist_btn.click(delay=150)
            filled_heart = self.page.locator('#yith-wcwl-icon-heart').first
            filled_heart.wait_for(state="visible", timeout=4000)
            success = True
        except Exception:
            success = False
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")
        return item_name if success else None

    @allure.step("Scroll to load all products")
    def scroll_to_load_all_products(self) -> int:
        last_count = 0
        retries = 0
        while retries < 5:
            self.page.keyboard.press("PageDown")
            self.page.wait_for_timeout(1000)
            current_count = self.page.locator(TeaPageLocators.PRODUCT_ITEM).count()
            if current_count > last_count:
                last_count = current_count
                retries = 0
            else:
                retries += 1
        print(f"--- Finished scrolling! Total products loaded: {last_count} ---")
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(1000)
        total_products = (
            self.page
            .locator(TeaPageLocators.PRODUCT_LIST)
            .locator(TeaPageLocators.PRODUCT_ITEM)
            .count()
        )
        return total_products

    def re_scroll_to_recover_products(self, total_products: int):
        for _ in range(25):
            self.page.mouse.wheel(0, 1000)
            self.page.wait_for_timeout(300)
            current_count = self.page.locator(TeaPageLocators.PRODUCT_ITEM).count()
            if current_count >= total_products:
                print(f"Recovered {current_count} items in DOM.")
                break
        self.page.wait_for_timeout(1000)

    @allure.step("Add simple product to cart at index {index}")
    def add_simple_product_by_index(self, index: int) -> str:
        product_list = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        simple_products = product_list.locator(TeaPageLocators.SIMPLE_PRODUCT_ITEM)
        product_item = simple_products.nth(index)
        product_item.scroll_into_view_if_needed()
        product_item.hover()
        add_to_cart_btn = product_item.locator(TeaPageLocators.ADD_TO_CART_BTN)
        add_to_cart_btn.wait_for(state="visible")
        item_name = product_item.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()
        count_locator = self.page.locator(TeaPageLocators.CART_COUNT)
        current_count = int(count_locator.inner_text().strip() or "0")
        add_to_cart_btn.click(force=True)
        self.page.locator(f'span.count-item:has-text("{current_count + 1}")').wait_for(
            state="visible", timeout=5000
        )
        return item_name