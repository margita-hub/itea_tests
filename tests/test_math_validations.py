import pytest
import pytest_check as check
from pages.locators import TeaPageLocators
from utils.math_helpers import calculate_qty_for_free_shipping
from config.config import TEA_URL

pytestmark = pytest.mark.math


class TestCartMath:

    def test_free_shipping_calculator(self, setup_all_page):
        """Verify free shipping math calculation is correct."""
        home_page = setup_all_page["home"]
        tea_page = setup_all_page["tea"]

        home_page.click_tea_menu()
        tea_page.page.wait_for_timeout(2000)

        shipping_tracker = tea_page.page.locator('.oceanwp-woo-left-to-free')
        initial_text = shipping_tracker.inner_text()
        initial_shipping_left = tea_page.extract_price(initial_text)
        print(f"\n--- Initial Amount needed: {initial_shipping_left} ---")

        first_product = tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first
        first_product.scroll_into_view_if_needed()

        title = first_product.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()
        price_text = first_product.locator('.price').inner_text()
        item_price = tea_page.extract_price(price_text)
        print(f"Adding '{title}' - Price: {item_price}")

        first_product.hover()
        tea_page.page.wait_for_timeout(500)
        cart_btn = first_product.locator(TeaPageLocators.ADD_TO_CART_BTN)
        cart_btn.click()

        tea_page.page.locator('span.count-item:has-text("1")').wait_for(state="visible", timeout=5000)
        tea_page.page.wait_for_timeout(1000)

        new_text = shipping_tracker.inner_text()
        new_shipping_left = tea_page.extract_price(new_text)
        expected_left = initial_shipping_left - item_price

        check.equal(
            round(new_shipping_left, 2),
            round(expected_left, 2),
            f"MATH BUG! Expected ₪{expected_left} left, but UI shows ₪{new_shipping_left}!"
        )
        print("Free Shipping Math works!")