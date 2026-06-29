import pytest
from utils.data_reader import load_products_from_db


EXPECTED_PRODUCTS = load_products_from_db()

pytestmark = pytest.mark.database
class TestDatabaseValidation:

    @pytest.mark.parametrize("tea_data", EXPECTED_PRODUCTS)
    def test_verify_tea_prices_from_json(self, setup_all_page_session, tea_data):
        #Reads expected products from db.json and verifies they exist on the live website with the correct price
        tea_page = setup_all_page_session["tea"]

        expected_name = tea_data["name"]
        expected_price = tea_data["price"]

        print(f"\n--- Checking DB Product: {expected_name} | Expected Price: ₪{expected_price} ---")

        tea_page.load()

        # Scroll to the bottom to ensure lazy-loaded items appear in the DOM
        tea_page.scroll_to_load_all_products()
        tea_page.page.locator("li.product").first.wait_for(state="visible")

        # Use filter to avoid Strict Mode Violation if multiple teas match
        product_card = tea_page.page.locator("li.product").filter(has_text=expected_name).first

        product_card.wait_for(state="visible", timeout=5000)
        assert product_card.is_visible(), f"DATA BUG: Could not find '{expected_name}' on the website!"

        price_text = product_card.locator(".price").inner_text()

        # Clean the price string (e.g., "₪ 56.00" -> 56.0)
        clean_price_text = "".join(c for c in price_text if c.isdigit() or c == '.')
        actual_price = float(clean_price_text)
        print(f"Found {expected_name} on site for ₪{actual_price}")

        assert actual_price == expected_price, (
            f"MATH BUG! Price mismatch for {expected_name}.\n"
            f"Expected (DB): ₪{expected_price}, Actual (Website): ₪{actual_price}"
        )
        print(f"Data verified: {expected_name} is exactly ₪{actual_price}")