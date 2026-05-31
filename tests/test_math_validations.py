import re
import pytest
from pages.locators import TeaPageLocators


def extract_price(price_text: str) -> float:
    """
    Extracts the active price from a WooCommerce string.
    Example 1: "₪200" -> 200.0
    Example 2 (Sale): "₪35.00 ₪30.00" -> 30.00 (Takes the last number!)
    """
    matches = re.findall(r'\d+\.?\d*', price_text)
    if matches:
        return float(matches[-1])
    return 0.0


class TestCartMath:

    def test_free_shipping_calculator(self, setup_all_page):
        home_page = setup_all_page["home"]
        tea_page = setup_all_page["tea"]

        # 1. Start at the Tea Grid
        home_page.navigate_to("https://itea.co.il/en/tea/")
        tea_page.page.wait_for_timeout(2000)

        # 2. Locate the Free Shipping Tracker in the header/cart area
        shipping_tracker = tea_page.page.locator('.oceanwp-woo-left-to-free')

        # Read the initial "Left to Free" amount (e.g., 200)
        initial_text = shipping_tracker.inner_text()
        initial_shipping_left = extract_price(initial_text)
        print(f"\n--- Initial Amount needed for Free Shipping: {initial_shipping_left} ---")

        # 3. Find the very first product on the page
        first_product = tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first
        first_product.scroll_into_view_if_needed()

        # Get its name and price
        title = first_product.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()
        price_text = first_product.locator('.price').inner_text()

        # Convert the price text to a math float!
        item_price = extract_price(price_text)
        print(f"🛒 Adding '{title}' to cart. Price: {item_price}")

        # 4. Add the item to the cart
        first_product.hover()
        tea_page.page.wait_for_timeout(500)  # Wait for animation
        cart_btn = first_product.locator(TeaPageLocators.ADD_TO_CART_BTN)
        cart_btn.click()

        # 5. Wait for WooCommerce AJAX to finish adding the item
        # The cart bubble will update to '1' when it's done!
        tea_page.page.locator('span.count-item:has-text("1")').wait_for(state="visible", timeout=5000)

        # Wait a tiny bit more for the Free Shipping text to finish its update animation
        tea_page.page.wait_for_timeout(1000)

        # 6. Read the NEW "Left to Free" amount
        new_text = shipping_tracker.inner_text()
        new_shipping_left = extract_price(new_text)
        print(f"--- New Amount needed for Free Shipping: {new_shipping_left} ---")

        # 7. THE MATHEMATICAL ASSERTION
        expected_left = initial_shipping_left - item_price

        # We use round(x, 2) because Python float math can be weird (e.g., 200.0 - 35.5 = 164.5000000001)
        assert round(new_shipping_left, 2) == round(expected_left, 2), (
            f"MATH BUG DETECTED! Expected {expected_left} left for free shipping, "
            f"but the UI calculated {new_shipping_left}!"
        )
        print("✅ Free Shipping Math works perfectly!")
