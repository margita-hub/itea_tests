from playwright.sync_api import Page
from pages.base_page import BasePage

class ProductPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def select_option_from_dropdown(self, option_index: int):
        option_dropdown = self.page.locator('select[name*="bundle_attribute"]').first
        option_dropdown.wait_for(state="visible", timeout=5000)
        option_dropdown.select_option(index=option_index)
        self.page.wait_for_timeout(500)

        selected_text = option_dropdown.evaluate('el => el.options[el.selectedIndex].text')
        print(f"Option selected: {selected_text}")

        toast = self.page.locator('.woocommerce-message').first
        if toast.count() > 0 and toast.is_visible():
            print(f"Toast after option select: {toast.inner_text()}")


    def get_error_message(self) -> str:
        msg = self.page.locator('span.msg-content')
        if msg.is_visible():
            return msg.inner_text()
        return ""


    def set_quantity(self, quantity: int):
        qty_input = self.page.locator('input[name="quantity"]')
        qty_input.wait_for(state="visible", timeout=5000)
        qty_input.fill(str(quantity))
        qty_input.blur()
        self.page.wait_for_timeout(500)


    def get_quantity(self) -> int:
        qty_input = self.page.locator('input[name="quantity"]')
        qty_input.wait_for(state="visible", timeout=5000)
        return int(qty_input.input_value())



    def click_add_to_wishlist(self):
        wishlist_btn = self.page.locator('span.yith-wcwl-add-to-wishlist-button__label')
        wishlist_btn.wait_for(state="visible", timeout=5000)
        wishlist_btn.click()


    def is_added_to_wishlist(self) -> bool:
        heart = self.page.locator('#yith-wcwl-icon-heart-outline').first
        return heart.is_visible()


    def is_added_to_cart_confirmation_visible(self) -> bool:
        return self.view_cart_link.is_visible()


    @property
    def view_cart_link(self):
        return self.page.locator('a.added_to_cart.wc-forward')

    def view_cart(self):
        self.view_cart_link.click()

    def clear_options(self):
        clear_btn = self.page.locator('a.reset_variations')
        if clear_btn.is_visible():
            clear_btn.click()

    def click_add_to_cart(self):
        add_btn = self.page.locator('button[name="add-to-cart"]')
        add_btn.wait_for(state="visible", timeout=5000)
        add_btn.click()
        self.page.wait_for_timeout(1000)

        toast = self.page.locator('.woocommerce-message').first
        if toast.count() > 0 and toast.is_visible():
            print(f" Toast: {toast.inner_text()}")


