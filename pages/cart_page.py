from playwright.sync_api import Page
from config.config import CART_URL
from pages.base_page import BasePage
from pages.locators import CartPageLocators
import allure


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Load cart page")
    def load(self):
        self.navigate_to(CART_URL)

    @allure.step("Count items in cart")
    def count_items(self) -> int:
        return self.page.locator('a.remove').count()

    @allure.step("Remove first item from cart")
    def remove_first_item(self):
        self.page.locator('a.remove').first.click()
        self.page.locator('.blockUI.blockOverlay').first.wait_for(state="hidden", timeout=10000)

    @allure.step("Remove all items from cart")
    def remove_all_items(self):
        while self.count_items() > 0:
            self.remove_first_item()

    @allure.step("Get cart item names")
    def get_cart_item_names(self) -> list[str]:
        self.page.locator("td.product-name").first.wait_for(timeout=5000)
        return self.page.locator("td.product-name a").all_inner_texts()

    @allure.step("Get cart total")
    def get_cart_total(self) -> float:
        total = self.page.locator("tr.order-total td > strong .woocommerce-Price-amount").first
        total.wait_for(timeout=5000)
        return self.extract_price(total.inner_text())

    @allure.step("Check empty cart message visible")
    def is_empty_message_visible(self) -> bool:
        return self.page.locator('.cart-empty').is_visible()

    @allure.step("Check cart totals visible")
    def is_cart_totals_visible(self) -> bool:
        return self.page.get_by_role("heading", name="Cart totals").is_visible()

    @allure.step("Update item quantity to {quantity}")
    def update_item_quantity(self, item_index: int, quantity: int):
        qty_input = self.page.locator(CartPageLocators.QUANTITY_INPUT).nth(item_index)
        qty_input.wait_for(state="visible", timeout=5000)
        qty_input.click(click_count=3)
        qty_input.fill(str(quantity))
        qty_input.dispatch_event("change")
        qty_input.press("Tab")
        update_btn = self.page.locator(CartPageLocators.UPDATE_CART_BTN)
        update_btn.wait_for(state="visible", timeout=5000)
        update_btn.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Get item subtotal at index {item_index}")
    def get_item_subtotal(self, item_index: int) -> float:
        subtotals = self.page.locator('td.product-subtotal .woocommerce-Price-amount')
        subtotal = subtotals.nth(item_index)
        subtotal.wait_for(timeout=5000)
        return self.extract_price(subtotal.inner_text())

    @allure.step("Increase quantity at index {item_index}")
    def increase_quantity(self, item_index: int):
        self.page.locator('a.plus').nth(item_index).click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Decrease quantity at index {item_index}")
    def decrease_quantity(self, item_index: int):
        self.page.locator('a.minus').nth(item_index).click()
        self.page.wait_for_load_state("networkidle")