import pytest
from pages.locators import TeaPageLocators

class TestCategoryGrids:

    #@pytest.mark.xfail(reason="Known Bug: Missing wishlist buttons")
    def test_all_products_have_wishlist_buttons(self, setup_all_page):
        home_page = setup_all_page["home"]
        tea_page = setup_all_page["tea"]

        home_page.click_tea_menu()
        tea_page.page.wait_for_load_state()

        # --- SCROLL TO BOTTOM TO LOAD ALL PRODUCTS ---
        # We loop 10 times, scrolling down a bit each time
        for _ in range(15):
            tea_page.page.mouse.wheel(0, 1000)
            tea_page.page.wait_for_timeout(500)  # Give WooCommerce time to load the images!

        # Scroll back to the top just to be safe
        tea_page.page.evaluate("window.scrollTo(0, 0)")
        tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")


        product_list = tea_page.page.locator(TeaPageLocators.PRODUCT_LIST)
        all_products = product_list.locator(TeaPageLocators.PRODUCT_ITEM)

        total_products_count = all_products.count()
        broken_products = []

        print(f"\n--- FOUND {total_products_count} TOTAL PRODUCTS ---")

        for i in range(total_products_count):
            product = all_products.nth(i)

            # We MUST scroll to the specific product before checking if its heart is visible!
            product.scroll_into_view_if_needed()

            title = product.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()
            heart_btn = product.locator(TeaPageLocators.ADD_TO_WISHLIST_BTN)

            if heart_btn.count() == 0:
                broken_products.append(f"{title} (No HTML)")
            elif not heart_btn.is_visible():
                broken_products.append(f"{title} (Hidden)")

        assert len(broken_products) == 0, (
            f"UI BUG DETECTED: {len(broken_products)} out of {total_products_count} "
            f"products are missing the Wishlist Heart button!\n"
            f"Broken products: {broken_products}"
        )


    #@pytest.mark.xfail(reason="Known Bug: Missing wishlist buttons on Teaware page too")
    def test_teaware_products_have_wishlist_buttons(self, setup_all_page):
        home_page = setup_all_page["home"]
        teaware_page = setup_all_page["teaware"]  # Make sure this matches your conftest!

        home_page.navigate_to("https://itea.co.il/en/")

        # We need to add a click_teaware_menu() method to home_page!
        home_page.navigate_to("https://itea.co.il/en/teaware/")
        teaware_page.page.wait_for_timeout(2000)

        # Scroll to load all products
        for _ in range(15):
            teaware_page.page.mouse.wheel(0, 1000)
            teaware_page.page.wait_for_timeout(500)

        # Note: We can reuse TeaPageLocators here because the WooCommerce grid HTML is identical across all categories!
        product_list = teaware_page.page.locator(TeaPageLocators.PRODUCT_LIST)
        all_products = product_list.locator(TeaPageLocators.PRODUCT_ITEM)
        total_products_count = all_products.count()
        broken_products = []

        for i in range(total_products_count):
            product = all_products.nth(i)
            product.scroll_into_view_if_needed()

            title = product.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()
            heart_btn = product.locator(TeaPageLocators.ADD_TO_WISHLIST_BTN)

            if heart_btn.count() == 0:
                broken_products.append(f"{title} (No HTML)")
            elif not heart_btn.is_visible():
                broken_products.append(f"{title} (Hidden)")

        assert len(
            broken_products) == 0, f"UI BUG DETECTED: {len(broken_products)} missing wishlist buttons! Broken: {broken_products}"
