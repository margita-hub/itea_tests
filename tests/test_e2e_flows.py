import pytest
import re
from config.config import VALID_CREDENTIALS
from pages.locators import TeaPageLocators
from tests.test_math_validations import extract_price
from utils.bug_reporter import BugReporter


def test_add_multiple_items_to_cart(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    home_page.navigate_to("https://itea.co.il/en/")
    home_page.click_tea_menu()
    tea_page.page.wait_for_timeout(2000)

    initial_shipping_left = home_page.get_amount_left_for_free_shipping()
    print(f"\n--- Initial Free Shipping Target: ₪{initial_shipping_left} ---")

    expected_teas = []
    total_cart_value = 0.0

    product_1 = tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).nth(0)
    price_1 = tea_page.get_product_price(product_1)
    tea_1 = tea_page.add_item_to_cart_by_index(0)
    expected_teas.append(tea_1)
    total_cart_value += price_1
    print(f"Added {tea_1} for ₪{price_1}")

    product_2 = tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).nth(2)
    price_2 = tea_page.get_product_price(product_2)
    tea_2 = tea_page.add_item_to_cart_by_index(2)
    expected_teas.append(tea_2)
    total_cart_value += price_2
    print(f"Added {tea_2} for ₪{price_2}")

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
        f"✅ Free Shipping Math Verified! (Started: {initial_shipping_left}, Added: {total_cart_value}, Left: {current_shipping_left})")
    # ----------------------

    # Navigate to Cart explicitly to avoid header visibility issues
    home_page.navigate_to("https://itea.co.il/en/cart/")

    items_in_cart = cart_page.get_cart_item_names()
    for expected_tea in expected_teas:
        assert expected_tea in items_in_cart, f"Missing {expected_tea} in cart! Cart has: {items_in_cart}"


def test_smart_discount_shopping(setup_all_page):
    """
    1. Scan the page for all sale items
    2. If the discount is >= 20%, Add to Cart
    3. If the discount is < 20%, Add to Wishlist via Product Page
    4. Print a summary of our automated shopping spree!
    5. Verify the actual Cart and Wishlist pages match our summary!
    """
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]

    home_page.navigate_to("https://itea.co.il/en/")
    home_page.click_tea_menu()
    tea_page.page.wait_for_timeout(2000)

    print("\n--- Scrolling to bottom to load ALL products... ---")

    last_count = 0
    retries = 0

    while retries < 5:
        # Hit PageDown to scroll naturally
        tea_page.page.keyboard.press("PageDown")
        tea_page.page.wait_for_timeout(1000)  # Wait 1 full second for AJAX to load images

        # Count how many products are currently in the DOM
        current_count = tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).count()

        if current_count > last_count:
            # We found more products! Keep scrolling!
            last_count = current_count
            retries = 0
        else:
            # The number of products didn't increase.
            # We might be at the bottom, so we add to the retry counter.
            retries += 1

    print(f"--- Finished scrolling! Total products loaded: {last_count} ---")
    # ---------------------------

    tea_page.page.evaluate("window.scrollTo(0, 0)")
    tea_page.page.wait_for_timeout(1000)
    product_list = tea_page.page.locator(TeaPageLocators.PRODUCT_LIST)
    all_products = product_list.locator(TeaPageLocators.PRODUCT_ITEM)
    total_products = all_products.count()

    # --- NEW: PULL ALL DISCOUNTS FIRST ---
    # We count exactly how many sale items are in the DOM before we start clicking!
    expected_sale_count = tea_page.page.locator('li.product span.onsale').count()
    print(f"\n--- EXPECTED TO FIND {expected_sale_count} SALE ITEMS! ---")
    # -------------------------------------

    cart_items = []
    wishlist_items = []

    # --- NEW: MATH TRACKING START ---
    initial_shipping_left = home_page.get_amount_left_for_free_shipping()
    total_cart_value_added = 0.0
    print(f"\n--- Initial Free Shipping Target: ₪{initial_shipping_left} ---")
    # --------------------------------

    #  Loop through all products
    for i in range(total_products):
        # ALWAYS fetch a completely fresh product list on every single loop!
        # This completely eliminates "Stale Element" issues after navigating back!
        product_list = tea_page.page.locator(TeaPageLocators.PRODUCT_LIST)
        all_products = product_list.locator(TeaPageLocators.PRODUCT_ITEM)
        product = all_products.nth(i)
        
        # Scroll to it
        product.scroll_into_view_if_needed()
        
        sale_badge = product.locator('span.onsale')

        if sale_badge.count() > 0 and sale_badge.is_visible():
            sale_text = sale_badge.inner_text().strip()
            title = product.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()

            # FREEZE THE BROWSER HERE!
            #breakpoint()

            # Extract just the numbers from the text
            match = re.search(r'\d+', sale_text)

            if match:
                discount = int(match.group())
                print(f"\n🛒 Found '{title}' with a {discount}% discount!")

                # 3. CONDITIONAL LOGIC
                if discount >= 20:
                    print(f"   --> Discount is >= 20%. Adding to CART.")
                    
                    # --- NEW: MATH TRACKING INSIDE LOOP ---
                    item_price = tea_page.get_product_price(product)
                    total_cart_value_added += item_price
                    print(f"   --> Item Price: ₪{item_price} (Running Total: ₪{total_cart_value_added})")
                    # --------------------------------------
                    
                    tea_page.add_item_to_cart_by_index(i)
                    cart_items.append(title)
                else:
                    print(f"   --> Discount is < 20%. Adding to WISHLIST via Product Page.")

                    # Call our new method, passing the INDEX!
                    success = tea_page.add_item_to_wishlist_via_product_page(i)
                    
                    if not success:
                        print(f"   ⚠️ WARNING: Failed to add '{title}' to Wishlist on its details page.")
                    else:
                        wishlist_items.append(title)

                    # CRITICAL FIX: We just came back from the product page.
                    # The DOM has reset! We must scroll down again to force lazy-loading!
                    # (Note: we don't need to re-locate here anymore because the top of the loop does it!)
                    print(f"   --> Scrolling back down to restore {total_products} items...")
                    for _ in range(25):
                        tea_page.page.mouse.wheel(0, 1000)
                        tea_page.page.wait_for_timeout(300)

                        current_count = tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).count()
                        if current_count >= total_products:
                            print(f"   --> Successfully recovered {current_count} items in DOM.")
                            break

                    tea_page.page.wait_for_timeout(1000)


    # Print Summary
    total_processed = len(cart_items) + len(wishlist_items)
    print("\n=========================================")
    print("        SMART SHOPPING SUMMARY           ")
    print("=========================================")
    print(f"Items Added to Cart: {len(cart_items)}")
    print(f"Items Added to Wishlist: {len(wishlist_items)}")
    print(f"Total Processed: {total_processed} / {expected_sale_count}")
    
    # THE BIG ASSERTION!
    assert total_processed == expected_sale_count, (
        f"CRITICAL LOOP BUG! We expected to find {expected_sale_count} sale items, "
        f"but we only processed {total_processed}!"
    )

    # --- NEW: MATHEMATICAL ASSERTION FOR FREE SHIPPING ---
    print("\nVerifying Free Shipping Math...")
    # Give the header one last second to finish any CSS updating
    tea_page.page.wait_for_timeout(1500)
    
    current_shipping_left = home_page.get_amount_left_for_free_shipping()
    expected_shipping_left = initial_shipping_left - total_cart_value_added
    
    # If expected drops below 0, it means we hit Free Shipping. 
    # The UI tracker will usually disappear or show 0.
    if expected_shipping_left < 0:
        expected_shipping_left = 0.0
        
    assert round(current_shipping_left, 2) == round(expected_shipping_left, 2), (
        f"MATH BUG! We started needing ₪{initial_shipping_left} and added ₪{total_cart_value_added} to the cart. "
        f"Expected to see ₪{expected_shipping_left} left, but the header says: ₪{current_shipping_left}"
    )
    print(f"✅ Free Shipping Math Verified! (Started: {initial_shipping_left}, Added: {total_cart_value_added}, Left: {current_shipping_left})")
    # -----------------------------------------------------

    #  VALIDATE THE CART!
    if len(cart_items) > 0:
        print("\nVerifying Cart Page...")
        cart_page = setup_all_page["cart"]

        home_page.navigate_to("https://itea.co.il/en/cart/")

        actual_cart_contents = cart_page.get_cart_item_names()

        for item in cart_items:
            assert item in actual_cart_contents, f"CRITICAL BUG: '{item}' was missing from the Cart Page!"
        print("✅ Cart validation passed!")

    # VALIDATE THE WISHLIST!
    if len(wishlist_items) > 0:
        print("\nVerifying Wishlist Page...")
        wishlist_page = setup_all_page["wishlist"]

        home_page.navigate_to("https://itea.co.il/en/wishlist/")

        actual_wishlist_contents = wishlist_page.get_wishlist_item_names()

        for item in wishlist_items:
            assert item in actual_wishlist_contents, f"CRITICAL BUG: '{item}' was missing from the Wishlist Page!"
        print("✅ Wishlist validation passed!")

    home_page.navigate_to("https://itea.co.il/en/cart/")
def test_free_shipping_threshold_reached(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    home_page.navigate_to("https://itea.co.il/en/tea/")
    tea_page.page.wait_for_timeout(2000)

    # 1. Get Initial Target (Should be ₪200)
    initial_shipping_left = home_page.get_amount_left_for_free_shipping()
    print(f"--- Initial Free Shipping Target: ₪{initial_shipping_left} ---")

    # 2. Add the first item to the cart
    product_1 = tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).nth(0)
    tea_1 = tea_page.add_item_to_cart_by_index(0)

    home_page.navigate_to("https://itea.co.il/en/cart/")
    cart_page.page.wait_for_timeout(2000)

    # 4. Change the quantity of the item to 10 (guaranteed to be > ₪200)
    print(f"🛒 Increasing quantity of {tea_1} to 10...")
    qty_input = cart_page.page.locator('input.qty').first
    qty_input.fill("10")
    qty_input.press("Enter")

    # Wait for the WooCommerce AJAX cart update to finish loading
    # ADD .first HERE TOO!
    cart_page.page.locator('.blockUI.blockOverlay').first.wait_for(state="hidden", timeout=10000)

    cart_page.page.wait_for_timeout(1500)  # Give CSS time to re-render

    # 5. Check what happens to the Free Shipping tracker!
    tracker = home_page.page.locator('.oceanwp-woo-left-to-free').first

    # When free shipping is reached, the UI usually changes state entirely.
    # It either disappears, or the text changes to "You have Free Shipping!"

    if tracker.is_visible():
        final_text = tracker.inner_text().lower()
        print(f"--- Tracker changed to: '{final_text}' ---")

        # Verify it no longer asks for money!
        assert "₪" not in final_text or extract_price(final_text) == 0.0, (
            "UI BUG! The cart is over ₪200, but the tracker is still asking for money!"
        )
        assert "free" in final_text or "congratulations" in final_text, (
            "UI BUG! The free shipping success message did not appear!"
        )
    else:
        print("✅ Tracker disappeared completely (Expected behavior for Free Shipping!)")

    # 6. Verify Free Shipping is actually an option in the Cart Totals table!
    shipping_options = cart_page.page.locator('#shipping_method').inner_text().lower()

    # We must check for "free" in the context of the delivery methods!
    assert "cheetah: free" in shipping_options or "delivery: free" in shipping_options, (
        f"CRITICAL BUG: Cart is >₪200 but Free delivery is not available! Options found: {shipping_options}"
    )
    print("✅ Free Delivery option is available at checkout!")

def test_empty_cart_behavior(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    # 1. Add an item to the cart first
    home_page.navigate_to("https://itea.co.il/en/tea/")
    tea_page.page.wait_for_timeout(2000)

    tea_page.add_item_to_cart_by_index(0)
    tea_page.page.wait_for_timeout(1000)

    # 2. Go to the cart
    home_page.navigate_to("https://itea.co.il/en/cart/")
    cart_page.page.wait_for_timeout(2000)

    # 3. Click the "Remove" button (Usually a red 'X' in WooCommerce)
    remove_btn = cart_page.page.locator('a.remove').first
    assert remove_btn.is_visible(), "UI BUG: Could not find the remove (X) button!"

    print("\n🛒 Removing item from cart...")
    remove_btn.click()

    # Wait for the WooCommerce AJAX cart update to finish loading
    # (Use .first because WooCommerce spawns multiple spinners!)
    cart_page.page.locator('.blockUI.blockOverlay').first.wait_for(state="hidden", timeout=10000)

    cart_page.page.wait_for_timeout(1000)

    # 4. Verify Empty Cart Message
    empty_message = cart_page.page.locator('.cart-empty').inner_text().lower()
    assert "empty" in empty_message, f"UI BUG: Expected empty message, got: '{empty_message}'"
    print("✅ Empty cart message displayed successfully!")

    # 5. Verify the "Return to shop" button exists
    return_to_shop_btn = cart_page.page.locator('.return-to-shop a.button')
    assert return_to_shop_btn.is_visible(), "UI BUG: 'Return to shop' button is missing!"

    # 6. Verify the Bubble count in the header is exactly '0'
    bubble_count = home_page.get_cart_item_count()
    assert bubble_count == 0, f"UI BUG: Cart is empty but bubble says {bubble_count}!"
    print("✅ Header bubble count is 0!")

    # 7. Verify the Free Shipping tracker resets back to 200!
    shipping_left = home_page.get_amount_left_for_free_shipping()
    assert round(shipping_left, 2) == 200.00, f"MATH BUG: Expected tracker to reset to 200, but it is {shipping_left}"
    print("✅ Free Shipping tracker successfully reset to 200!")