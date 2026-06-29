import pytest
import pytest_check as check
from pages.locators import TeaPageLocators

pytestmark = pytest.mark.select_options


@pytest.mark.parametrize("product_index,option_index,quantity", [
    (0, 1, 1),
    (0, 2, 2),
    (0, 3, 5),
    (1, 1, 1),
    (1, 2, 3),
])
def test_add_select_options_product_to_cart(setup_all_page, product_index, option_index, quantity):
    tea = setup_all_page["tea"]
    product = setup_all_page["product"]
    cart = setup_all_page["cart"]

    tea.load()
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.click_select_options_button_for_product(product_index)
    tea.page.wait_for_load_state("domcontentloaded")

    product.select_option_from_dropdown(option_index)
    check.is_false(bool(product.get_error_message()), "Error message shown after selecting option")

    product.set_quantity(quantity)
    check.equal(product.get_quantity(), quantity, f"Quantity should be {quantity}")

    product.click_add_to_cart()
    product.page.wait_for_timeout(1000)

    view_cart_link = product.page.locator('a.added_to_cart.wc-forward')
    view_cart_link.wait_for(state="visible", timeout=5000)
    view_cart_link.click()

    product.page.wait_for_load_state("domcontentloaded")
    product.page.wait_for_timeout(1000)

    check.is_in("/cart", product.page.url, "Should navigate to cart page")

    item_count = cart.count_items()
    check.greater_equal(item_count, 1, f"Cart should have at least 1 item, got {item_count}")
    check.is_true(cart.is_cart_totals_visible(), "Cart totals should be visible")

    print(f"Successfully added product (option {option_index}, qty {quantity})")


def test_select_option_required_error_message(setup_all_page):
    tea = setup_all_page["tea"]
    product = setup_all_page["product"]

    tea.load()
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.click_select_options_button_for_product(0)
    tea.page.wait_for_load_state("domcontentloaded")

    product.click_add_to_cart()

    error_msg = product.get_error_message()
    check.is_true(bool(error_msg), "Error message should appear when no option selected")
    check.is_in("choose", error_msg.lower(), f"Error should mention 'choose': {error_msg}")

    print(f"Error message correctly shown: {error_msg}")


def test_clear_option_selection(setup_all_page):
    tea = setup_all_page["tea"]
    product = setup_all_page["product"]

    tea.load()
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.click_select_options_button_for_product(0)
    tea.page.wait_for_load_state("domcontentloaded")

    product.select_option_from_dropdown(1)
    check.is_false(bool(product.get_error_message()), "Error shown after selecting option")

    product.clear_options()
    product.click_add_to_cart()
    check.is_true(bool(product.get_error_message()), "Error should appear after clearing options")

    print("Option clear functionality works correctly")


def test_add_select_options_product_to_wishlist(setup_all_page):
    tea = setup_all_page["tea"]
    product = setup_all_page["product"]

    tea.load()
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.click_select_options_button_for_product(0)
    tea.page.wait_for_load_state("domcontentloaded")

    product.click_add_to_wishlist()
    check.is_true(product.is_added_to_wishlist(), "Product should be added to wishlist")

    print("Successfully added select-options product to wishlist")