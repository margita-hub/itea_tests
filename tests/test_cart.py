from pages.locators import TeaPageLocators
import pytest
import pytest_check as check

pytestmark = pytest.mark.cart


def test_remove_items_one_by_one(setup_all_page):
    """Adding two items then removing each leaves the cart empty."""
    cart = setup_all_page["cart"]
    tea = setup_all_page["tea"]

    tea.load()
    tea.add_simple_product_by_index(0)
    tea.add_simple_product_by_index(2)
    cart.load()

    check.equal(cart.count_items(), 2, "Expected 2 items in cart")
    cart.remove_first_item()
    check.equal(cart.count_items(), 1, "Expected 1 item after removing one")
    cart.remove_first_item()
    check.is_true(cart.is_empty_message_visible(), "Empty cart message not shown")
    check.is_false(cart.is_cart_totals_visible(), "Cart totals still showing on empty cart")


def test_cart_shows_totals_with_items(setup_all_page):
    """A cart with items shows totals and NOT the empty message."""
    cart = setup_all_page["cart"]
    tea = setup_all_page["tea"]

    tea.load()
    tea.page.wait_for_load_state("domcontentloaded")
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.add_simple_product_by_index(0)
    cart.load()

    check.is_true(cart.is_cart_totals_visible(), "Cart has item but totals are missing")
    check.is_false(cart.is_empty_message_visible(), "Empty message shown with items in cart")


def test_add_simple_product_to_cart(setup_all_page):
    """Simple product adds to cart successfully."""
    tea  = setup_all_page["tea"]
    cart = setup_all_page["cart"]

    tea.load()
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.add_simple_product_by_index(0)
    cart.load()

    check.equal(cart.count_items(), 1, "Expected 1 item in cart")
    check.is_true(cart.is_cart_totals_visible(), "Cart totals not visible")


def test_add_options_required_product_to_cart(setup_all_page):
    """BUG TEST: Variable product should NOT add to cart without selecting options."""
    tea  = setup_all_page["tea"]
    cart = setup_all_page["cart"]

    tea.load()
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.click_select_options_button_for_product(0)
    cart.load()

    check.equal(cart.count_items(), 0, "BUG: Variable product added to cart without selecting options!")
    check.is_false(cart.is_cart_totals_visible(), "BUG: Cart totals showing on empty cart!")


def test_update_cart_item_quantity(setup_all_page):
    """Product is added to cart successfully."""
    tea = setup_all_page["tea"]
    cart = setup_all_page["cart"]

    tea.load()
    tea.add_simple_product_by_index(0)
    cart.load()

    check.equal(cart.count_items(), 1, "Expected 1 item in cart")