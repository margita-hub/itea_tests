


def test_remove_items_one_by_one(self, setup_all_page):
    # Adding two items then removing each leaves the cart empty.
    cart = setup_all_page["cart"]
    tea = setup_all_page["tea"]

    tea.load()
    tea.add_item_to_cart_by_index(0)
    tea.add_item_to_cart_by_index(2)
    cart.load()

    assert cart.count_items() == 2, f"Expected 2 items, found {cart.count_items()}"

    cart.remove_first_item()
    assert cart.count_items() == 1, "Item count did not drop to 1 after removing one"

    cart.remove_first_item()
    assert cart.is_empty_message_visible(), "Empty-cart message not shown after removing all"
    assert not cart.has_cart_totals(), "Cart totals still showing on empty cart"


def test_cart_shows_totals_with_items(self, setup_all_page):
    # A cart with items shows the totals and NOT the empty message.
    cart = setup_all_page["cart"]
    tea = setup_all_page["tea"]

    tea.load()
    tea.add_item_to_cart_by_index(0)
    cart.load()

    assert cart.has_cart_totals(), "Cart has an item but totals are missing"
    assert not cart.is_empty_message_visible(), "Empty message shown even though cart has an item"