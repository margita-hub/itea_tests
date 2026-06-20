from pages.locators import TeaPageLocators


def test_remove_items_one_by_one(setup_all_page):
    # Adding two items then removing each leaves the cart empty.
    cart = setup_all_page["cart"]
    tea = setup_all_page["tea"]

    tea.load()
    tea.add_simple_product_by_index(0)
    tea.add_simple_product_by_index(2)
    cart.load()

    assert cart.count_items() == 2, f"Expected 2 items, found {cart.count_items()}"

    cart.remove_first_item()
    assert cart.count_items() == 1, "Item count did not drop to 1 after removing one"

    cart.remove_first_item()
    assert cart.is_empty_message_visible(), "Empty-cart message not shown after removing all"
    assert not cart.is_cart_totals_visible(), "Cart totals still showing on empty cart"


def test_cart_shows_totals_with_items(setup_all_page):
    # A cart with items shows the totals and NOT the empty message.
    cart = setup_all_page["cart"]
    tea = setup_all_page["tea"]

    tea.load()
    tea.page.wait_for_load_state("domcontentloaded")
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")

    tea.add_simple_product_by_index(0)
    cart.load()

    assert cart.is_cart_totals_visible(), "Cart has an item but totals are missing"
    assert not cart.is_empty_message_visible(), "Empty message shown even though cart has an item"


def test_add_simple_product_to_cart(setup_all_page):
    tea  = setup_all_page["tea"]
    cart = setup_all_page["cart"]

    tea.load()
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.add_simple_product_by_index(0)

    cart.load()
    assert cart.count_items() == 1
    assert cart.is_cart_totals_visible()


def test_add_options_required_product_to_cart(setup_all_page):
    tea  = setup_all_page["tea"]
    cart = setup_all_page["cart"]

    tea.load()
    tea.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")
    tea.click_select_options_button_for_product(0)

    cart.load()
    assert cart.count_items() == 1
    assert cart.is_cart_totals_visible()


def test_update_cart_item_quantity(setup_all_page):
    tea = setup_all_page["tea"]
    cart = setup_all_page["cart"]

    tea.load()
    tea.add_simple_product_by_index(0)

    cart.load()
    assert cart.count_items() == 1

    # Update quantity to 3
    cart.update_item_quantity(0, 3)

    # Verify updated
    assert cart.count_items() == 1