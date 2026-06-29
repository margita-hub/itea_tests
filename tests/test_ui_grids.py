import pytest
import pytest_check as check
from pages.locators import TeaPageLocators

pytestmark = pytest.mark.ui


class TestCategoryGrids:

    def test_all_products_have_wishlist_buttons(self, setup_all_page_session):
        """All tea products should have wishlist heart buttons."""
        home_page = setup_all_page_session["home"]
        tea_page = setup_all_page_session["tea"]

        home_page.click_tea_menu()
        tea_page.page.wait_for_load_state()

        for _ in range(15):
            tea_page.page.mouse.wheel(0, 1000)
            tea_page.page.wait_for_timeout(500)

        tea_page.page.evaluate("window.scrollTo(0, 0)")
        tea_page.page.locator(TeaPageLocators.PRODUCT_ITEM).first.wait_for(state="visible")

        product_list = tea_page.page.locator(TeaPageLocators.PRODUCT_LIST)
        all_products = product_list.locator(TeaPageLocators.PRODUCT_ITEM)
        total_products_count = all_products.count()
        broken_products = []

        print(f"\n--- FOUND {total_products_count} TOTAL PRODUCTS ---")

        for i in range(total_products_count):
            product = all_products.nth(i)
            product.scroll_into_view_if_needed()
            title = product.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()
            heart_btn = product.locator(TeaPageLocators.ADD_TO_WISHLIST_BTN)
            if heart_btn.count() == 0:
                broken_products.append(f"{title} (No HTML)")
            elif not heart_btn.is_visible():
                broken_products.append(f"{title} (Hidden)")

        check.equal(len(broken_products), 0,
            f"UI BUG: {len(broken_products)}/{total_products_count} products missing wishlist button!\n{broken_products}")


    def test_teaware_products_have_wishlist_buttons(self, setup_all_page_session):
        """All teaware products should have wishlist heart buttons."""
        home_page = setup_all_page_session["home"]
        teaware_page = setup_all_page_session["teaware"]

        home_page.click_teaware_menu()
        teaware_page.page.wait_for_timeout(2000)

        for _ in range(15):
            teaware_page.page.mouse.wheel(0, 1000)
            teaware_page.page.wait_for_timeout(500)

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

        check.equal(len(broken_products), 0,
            f"UI BUG: {len(broken_products)} missing wishlist buttons! {broken_products}")