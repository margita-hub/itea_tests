from playwright.sync_api import Page
from playwright.sync_api import expect
from config.config import CART_URL
from pages.base_page import BasePage
from pages.locators import CartPageLocators

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def load(self):
            self.navigate_to(CART_URL)  # uses BasePage.navigate_to()

    def count_items(self) -> int:
        #How many product are currently in the cart
        return self.page.locator('a.remove').count()

    def remove_first_item(self):
        #Remove the first item and wait for the AJAX update to finish.
        self.page.locator('a.remove').first.click()
        self.page.locator('.blockUI.blockOverlay').first.wait_for(state="hidden", timeout=10000)

    def remove_all_items(self):
        #Remove items one by one until the cart is empty.
        while self.count_items() > 0:
            self.remove_first_item()

    def get_cart_item_names(self) -> list[str]:
        self.page.locator("td.product-name").first.wait_for(timeout=5000)
        return self.page.locator("td.product-name a").all_inner_texts()

    def get_cart_total(self) -> float:
        total = self.page.locator("tr.order-total td > strong .woocommerce-Price-amount").first
        total.wait_for(timeout=5000)
        return self.extract_price(total.inner_text())

    def is_empty_message_visible(self) -> bool:
        return self.page.locator('.cart-empty').is_visible()

    def is_cart_totals_visible(self) -> bool:
        return self.page.get_by_role("heading", name="Cart totals").is_visible()

    def update_item_quantity(self, item_index: int, quantity: int):
        qty_input = self.page.locator(CartPageLocators.QUANTITY_INPUT).nth(item_index)
        qty_input.wait_for(state="visible", timeout=5000)
        qty_input.click(click_count=3)
        qty_input.fill(str(quantity))

        # Trigger change event to enable Update cart button
        qty_input.dispatch_event("change")
        qty_input.press("Tab")  # ← triggers WooCommerce to enable button

        # Now button should be visible
        update_btn = self.page.locator(CartPageLocators.UPDATE_CART_BTN)
        update_btn.wait_for(state="visible", timeout=5000)
        update_btn.click()
        self.page.wait_for_load_state("networkidle")

    def get_item_subtotal(self, item_index: int) -> float:
        subtotals = self.page.locator('td.product-subtotal .woocommerce-Price-amount')
        subtotal = subtotals.nth(item_index)
        subtotal.wait_for(timeout=5000)
        return self.extract_price(subtotal.inner_text())

    def increase_quantity(self, item_index: int):
        """Click + button to increase quantity."""
        plus_btns = self.page.locator('a.plus')
        plus_btns.nth(item_index).click()
        self.page.wait_for_load_state("networkidle")

    def decrease_quantity(self, item_index: int):
        """Click - button to decrease quantity."""
        minus_btns = self.page.locator('a.minus')
        minus_btns.nth(item_index).click()
        self.page.wait_for_load_state("networkidle")