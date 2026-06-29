from Services.shopping_service import ShoppingService
from pages.locators import TeaPageLocators
from utils.math_helpers import calculate_qty_for_free_shipping
import pytest
import pytest_check as check

pytestmark = pytest.mark.e2e


def test_add_multiple_items_to_cart(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    home_page.click_tea_menu()
    tea_page.page.wait_for_load_state("networkidle")

    print("\n--- Scrolling to load all teas before adding to cart ---")
    tea_page.scroll_to_load_all_products()

    initial_shipping_left = home_page.get_amount_left_for_free_shipping()
    print(f"\n--- Initial Free Shipping Target: ₪{initial_shipping_left} ---")

    expected_teas = []
    total_cart_value = 0.0
    indexes_to_add = [0, 2]
    simple_products = tea_page.page.locator('li.product:has(a.product_type_simple)')

    for index in indexes_to_add:
        product = simple_products.nth(index)
        price = tea_page.get_product_price(product)
        tea_name = tea_page.add_simple_product_by_index(index)
        expected_teas.append(tea_name)
        total_cart_value += price
        print(f"Added {tea_name} for ₪{price}")

    current_count = home_page.get_cart_item_count()
    check.equal(current_count, 2, f"UI BUG: Cart bubble says {current_count}, but we added 2 items!")

    tea_page.page.wait_for_timeout(1000)
    current_shipping_left = home_page.get_amount_left_for_free_shipping()
    expected_shipping_left = initial_shipping_left - total_cart_value

    check.equal(
        round(current_shipping_left, 2),
        round(expected_shipping_left, 2),
        f"MATH BUG! Started ₪{initial_shipping_left}, added ₪{total_cart_value}, expected ₪{expected_shipping_left}, got ₪{current_shipping_left}"
    )

    cart_page.load()
    items_in_cart = cart_page.get_cart_item_names()
    for expected_tea in expected_teas:
        check.is_in(expected_tea, items_in_cart, f"Missing {expected_tea} in cart! Cart has: {items_in_cart}")


@pytest.mark.slow
def test_smart_discount_shopping(setup_all_page):
    home = setup_all_page["home"]
    tea = setup_all_page["tea"]

    tea.load()
    total = tea.scroll_to_load_all_products()

    summary = ShoppingService(tea, home).process_sale_items(total)

    check.equal(
        len(summary["cart_items"]) + len(summary["wishlist_items"]),
        summary["expected_sale_count"],
        "Sale items count mismatch!"
    )

    cart = setup_all_page["cart"]
    cart.load()
    cart_names = cart.get_cart_item_names()
    for item in summary["cart_items"]:
        check.is_in(item, cart_names, f"Missing {item} in cart!")

    wishlist = setup_all_page["wishlist"]
    wishlist.load()
    wishlist_names = wishlist.get_wishlist_item_names()
    for item in summary["wishlist_items"]:
        check.is_in(item, wishlist_names, f"Missing {item} in wishlist!")


def test_free_shipping_threshold_reached(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    tea_page.load()
    tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")

    first_simple = tea_page.page.locator('li.product:has(a.product_type_simple)').first
    item_price = tea_page.extract_price(first_simple.locator('.price').inner_text())
    print(f"Unit price: ₪{item_price}")

    initial_shipping_left = home_page.get_amount_left_for_free_shipping()
    print(f"--- Initial Free Shipping Target: ₪{initial_shipping_left} ---")

    tea_page.add_simple_product_by_index(0)
    cart_page.load()
    cart_page.page.locator('a.remove').first.wait_for(state="visible")

    qty_needed = calculate_qty_for_free_shipping(item_price)
    print(f"₪{item_price} per item — need qty {qty_needed} to exceed ₪200")

    qty_input = cart_page.page.locator('input.qty').first
    qty_input.fill(str(qty_needed))
    qty_input.press("Enter")

    cart_page.page.locator('.blockUI.blockOverlay').first.wait_for(state="hidden", timeout=10000)
    cart_page.page.reload()
    cart_page.page.wait_for_load_state("networkidle")

    tracker = home_page.page.locator('.oceanwp-woo-left-to-free').first

    if tracker.is_visible():
        final_text = tracker.inner_text().lower()
        print(f"Tracker text: '{final_text}'")
        check.is_true(
            "₪" not in final_text or home_page.extract_price(final_text) == 0.0,
            "UI BUG! Cart is over ₪200 but tracker still asking for money!"
        )
        check.is_true(
            "free" in final_text or "congratulations" in final_text,
            "UI BUG! Free shipping success message did not appear!"
        )
    else:
        print("Tracker disappeared — free shipping reached!")

    shipping_options = cart_page.page.locator('#shipping_method').inner_text().lower()
    check.is_true(
        "cheetah: free" in shipping_options or "delivery: free" in shipping_options,
        f"CRITICAL BUG: Cart >₪200 but Free delivery not available! Options: {shipping_options}"
    )
    print("Free Delivery option is available!")


def test_empty_cart_behavior(setup_all_page):
    home_page = setup_all_page["home"]
    tea_page = setup_all_page["tea"]
    cart_page = setup_all_page["cart"]

    tea_page.load()
    tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea_page.add_simple_product_by_index(0)

    cart_page.load()
    cart_page.page.locator('a.remove').first.wait_for(state="visible")

    remove_btn = cart_page.page.locator('a.remove').first
    check.is_true(remove_btn.is_visible(), "UI BUG: Remove button not found!")

    print("\n Removing item from cart...")
    remove_btn.click()

    cart_page.page.locator('.blockUI.blockOverlay').first.wait_for(state="hidden", timeout=10000)
    cart_page.page.locator('.cart-empty').wait_for(state="visible")

    empty_message = cart_page.page.locator('.cart-empty').inner_text().lower()
    check.is_in("empty", empty_message, f"UI BUG: Expected empty message, got: '{empty_message}'")
    print("Empty cart message displayed!")

    return_to_shop_btn = cart_page.page.locator('.return-to-shop a.button')
    check.is_true(return_to_shop_btn.is_visible(), "UI BUG: 'Return to shop' button missing!")

    bubble_count = home_page.get_cart_item_count()
    check.equal(bubble_count, 0, f"UI BUG: Cart empty but bubble says {bubble_count}!")
    print("Header bubble count is 0!")

    shipping_left = home_page.get_amount_left_for_free_shipping()
    check.equal(round(shipping_left, 2), 200.00, f"MATH BUG: Expected tracker reset to 200, got {shipping_left}")
    print("Free Shipping tracker reset to 200!")