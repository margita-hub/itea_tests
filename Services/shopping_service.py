# services/shopping_service.py

class ShoppingService:

    def __init__(self, tea_page, home_page):
        self.tea  = tea_page
        self.home = home_page

    def process_sale_items(self, total_products, discount_threshold=20):
        """
        Loop through all products, apply discount logic,
        return a summary dict.

        Reusable by any test that needs sale item processing.

        Returns:
            {
                "cart_items":             ["title1", "title2"],
                "wishlist_items":         ["title3"],
                "total_cart_value":       95.0,
                "initial_shipping_left":  200.0,
                "expected_sale_count":    3
            }
        """
        cart_items = []
        wishlist_items = []
        total_cart_value_added = 0.0
        initial_shipping_left = self.home.get_amount_left_for_free_shipping()
        expected_sale_count = self.tea.get_expected_sale_count()

        print(f"\n--- Initial Free Shipping Target: ₪{initial_shipping_left} ---")
        print(f"--- Expected sale items: {expected_sale_count} ---")

        for i in range(total_products):
            #product.scroll_into_view_if_needed()removing
            product = self.tea.get_product_at_index(i)

            try:
                product.scroll_into_view_if_needed()
            except Exception:
                # Products dropped out of DOM — re-scroll to recover
                self.tea.re_scroll_to_recover_products(total_products)
                product = self.tea.get_product_at_index(i)
                product.scroll_into_view_if_needed()


            if not self.tea.has_sale_badge(product):
                continue

            title = self.tea.get_product_title(product)
            discount = self.tea.get_sale_discount(product)

            if not discount:
                continue

            print(f"\n'{title}' — {discount}% discount")

            if discount >= discount_threshold:
                print(f"   --> >= {discount_threshold}%. Adding to CART.")
                item_price = self.tea.get_product_price(product)
                total_cart_value_added += item_price
                self.tea.add_simple_product_by_index(i)
                cart_items.append(title)

            else:
                print(f"   --> < {discount_threshold}%. Adding to WISHLIST.")
                success = self.tea.add_item_to_wishlist_via_product_page(i)
                if success:
                    wishlist_items.append(title)
                else:
                    print(f" Could not add '{title}' to wishlist.")
                self.tea.re_scroll_to_recover_products(total_products)

        return {
            "cart_items":           cart_items,
            "wishlist_items":       wishlist_items,
            "total_cart_value":     total_cart_value_added,
            "initial_shipping_left": initial_shipping_left,
            "expected_sale_count":  expected_sale_count,
        }