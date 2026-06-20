from Services.shopping_service import ShoppingService
from pages.cart_page import CartPage
from pages.locators import TeaPageLocators
from utils.math_helpers import calculate_qty_for_free_shipping


def test_add_multiple_items_to_cart(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    home_page.click_tea_menu()
    #tea_page.page.wait_for_timeout(2000)
    # Instead of wait_for_timeout(2000) after navigate_to or load()
    tea_page.page.wait_for_load_state("networkidle")

    # Scroll down to ensure all teas (like the 3rd one) are loaded into the DOM
    print("\n--- Scrolling to load all teas before adding to cart ---")
    tea_page.scroll_to_load_all_products()

    initial_shipping_left = home_page.get_amount_left_for_free_shipping()
    print(f"\n--- Initial Free Shipping Target: ₪{initial_shipping_left} ---")

    expected_teas = []
    total_cart_value = 0.0

    # loop through the indexes
    indexes_to_add = [0, 2]

    simple_products = tea_page.page.locator('li.product:has(a.product_type_simple)')

    for index in indexes_to_add:
        product = simple_products.nth(index)  # filter
        price = tea_page.get_product_price(product)  # reads price from simple product
        tea_name = tea_page.add_simple_product_by_index(index)  # adds same simple product

        expected_teas.append(tea_name)
        total_cart_value += price
        print(f"Added {tea_name} for ₪{price}")

    current_count = home_page.get_cart_item_count()
    assert current_count == 2, f"UI BUG: Cart bubble says {current_count}, but we added 2 items!"

    tea_page.page.wait_for_timeout(1000)  # Give CSS time to update
    current_shipping_left = home_page.get_amount_left_for_free_shipping()
    expected_shipping_left = initial_shipping_left - total_cart_value

    assert round(current_shipping_left, 2) == round(expected_shipping_left, 2), (
        f"MATH BUG! We started needing ₪{initial_shipping_left} and added ₪{total_cart_value} to the cart. "
        f"Expected to see ₪{expected_shipping_left} left, but the header says: ₪{current_shipping_left}"
    )
    print(
        f" Free Shipping Math Verified! (Started: {initial_shipping_left}, Added: {total_cart_value}, Left: {current_shipping_left})")
    # ----------------------

    # Navigate to Cart explicitly to avoid header visibility issues
    cart_page.load()

    items_in_cart = cart_page.get_cart_item_names()
    for expected_tea in expected_teas:
        assert expected_tea in items_in_cart, f"Missing {expected_tea} in cart! Cart has: {items_in_cart}"


def test_smart_discount_shopping(setup_all_page):
    home = setup_all_page["home"]
    tea = setup_all_page["tea"]

    tea.load()
    total = tea.scroll_to_load_all_products()

    # Using the Service Layer Pattern here.
    # One line replaces the entire loop ─> shopping_services -> Instead of writing complex loops in the test, we call ShoppingService to handle the business logic of finding sale items and separating them.
    summary = ShoppingService(tea, home).process_sale_items(total)

    assert len(summary["cart_items"]) + len(summary["wishlist_items"]) \
           == summary["expected_sale_count"]

    cart = setup_all_page["cart"]
    cart.load()
    for item in summary["cart_items"]:
        assert item in cart.get_cart_item_names()

    wishlist = setup_all_page["wishlist"]
    wishlist.load()
    for item in summary["wishlist_items"]:
        assert item in wishlist.get_wishlist_item_names()



def test_free_shipping_threshold_reached(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    tea_page.load()
    tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")

    # Get unit price BEFORE adding to cart
    first_simple = tea_page.page.locator('li.product:has(a.product_type_simple)').first
    item_price = tea_page.extract_price(first_simple.locator('.price').inner_text())
    print(f"Unit price: ₪{item_price}")

    initial_shipping_left = home_page.get_amount_left_for_free_shipping()
    print(f"--- Initial Free Shipping Target: ₪{initial_shipping_left} ---")

    # Add the first with button "add item" item to the cart
    tea_1 = tea_page.add_simple_product_by_index(0)

    cart_page.load()
    cart_page.page.locator('a.remove').first.wait_for(state="visible")

    # Now calculate using actual unit price
    qty_needed = calculate_qty_for_free_shipping(item_price)
    print(f"₪{item_price} per item — need qty {qty_needed} to exceed ₪200")

    qty_input = cart_page.page.locator('input.qty').first
    qty_input.fill(str(qty_needed))
    qty_input.press("Enter")

    # Wait for the WooCommerce AJAX cart update to finish loading
    # ADD .first HERE TOO!
    cart_page.page.locator('.blockUI.blockOverlay').first.wait_for(state="hidden", timeout=10000)

    # Tracker only updates on page reload — force it
    cart_page.page.reload()
    cart_page.page.wait_for_load_state("networkidle")

    # Define tracker AFTER reload so it reads fresh value
    tracker = home_page.page.locator('.oceanwp-woo-left-to-free').first

    # Debug prints
    print(f"qty_needed: {qty_needed}")
    print(f"cart total after qty change: {cart_page.get_cart_total()}")
    if tracker.is_visible():
        print(f"tracker text after qty change: '{tracker.inner_text()}'")
    else:
        print("Tracker disappeared — free shipping reached! ")

    # Check what happens to the Free Shipping tracker
    #tracker = home_page.page.locator('.oceanwp-woo-left-to-free').first

    # When free shipping is reached, the UI usually changes state entirely.
    # It disappears, or the text changes to "You have Free Shipping!"

    if tracker.is_visible():
        final_text = tracker.inner_text().lower()
        print(f"Tracker text: '{final_text}'")
        print(f"Price in tracker: {home_page.extract_price(final_text)}")

        assert "₪" not in final_text or home_page.extract_price(final_text) == 0.0, (
            "UI BUG! The cart is over ₪200, but the tracker is still asking for money!"
        )
        assert "free" in final_text or "congratulations" in final_text, (
            "UI BUG! The free shipping success message did not appear!"
        )
    else:
        print("Tracker disappeared — free shipping reached!")

    # Verify Free Shipping is actually an option in the Cart Totals table!
    shipping_options = cart_page.page.locator('#shipping_method').inner_text().lower()

    # We must check for "free" in the context of the delivery methods!
    assert "cheetah: free" in shipping_options or "delivery: free" in shipping_options, (
        f"CRITICAL BUG: Cart is >₪200 but Free delivery is not available! Options found: {shipping_options}"
    )
    print(" Free Delivery option is available at checkout!")

def test_empty_cart_behavior(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    # Add an item to the cart first
    tea_page.load()
    tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")

    tea_page.add_simple_product_by_index(0)
    tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")

    # Go to the cart
    cart_page.load()
    cart_page.page.locator('a.remove').first.wait_for(state="visible")

    # Click the "Remove" button (Usually a red 'X' in WooCommerce)
    remove_btn = cart_page.page.locator('a.remove').first
    assert remove_btn.is_visible(), "UI BUG: Could not find the remove (X) button!"

    print("\n🛒 Removing item from cart...")
    remove_btn.click()

    # Wait for the WooCommerce AJAX cart update to finish loading
    # (Use .first because WooCommerce spawns multiple spinners!)
    cart_page.page.locator('.blockUI.blockOverlay').first.wait_for(state="hidden", timeout=10000)
    # After AJAX overlay disappears
    cart_page.page.locator('.cart-empty').wait_for(state="visible")

    # Verify Empty Cart Message
    empty_message = cart_page.page.locator('.cart-empty').inner_text().lower()
    assert "empty" in empty_message, f"UI BUG: Expected empty message, got: '{empty_message}'"
    print(" Empty cart message displayed successfully!")

    # Verify the "Return to shop" button exists
    return_to_shop_btn = cart_page.page.locator('.return-to-shop a.button')
    assert return_to_shop_btn.is_visible(), "UI BUG: 'Return to shop' button is missing!"

    # Verify the Bubble count in the header is exactly '0'
    bubble_count = home_page.get_cart_item_count()
    assert bubble_count == 0, f"UI BUG: Cart is empty but bubble says {bubble_count}!"
    print(" Header bubble count is 0!")

    # Verify the Free Shipping tracker resets back to 200
    shipping_left = home_page.get_amount_left_for_free_shipping()
    assert round(shipping_left, 2) == 200.00, f"MATH BUG: Expected tracker to reset to 200, but it is {shipping_left}"
    print(" Free Shipping tracker successfully reset to 200!")