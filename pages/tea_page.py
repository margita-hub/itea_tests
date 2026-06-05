import re
from playwright.sync_api import Page

from config.config import TEA_URL
from pages.base_page import BasePage
from pages.locators import TeaPageLocators


class TeaPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    # ── Navigation ────────────────────────────────────────────────────────────

    def load(self):
        self.navigate_to(TEA_URL)

    def is_page_loaded(self) -> bool:
        title_locator = self.page.locator('h1.page-header-title')
        try:
            title_locator.wait_for(state="visible", timeout=5000)
            return "Tea" in title_locator.inner_text()
        except Exception:
            return False

    # ── Product helpers ───────────────────────────────────────────────────────

    def get_product_at_index(self, index: int):
        """
        Always fetch a fresh locator per loop iteration.
        Eliminates StaleElementReferenceException after navigation.
        """
        return (
            self.page
            .locator(TeaPageLocators.PRODUCT_LIST)
            .locator(TeaPageLocators.PRODUCT_ITEM)
            .nth(index)
        )

    def get_product_title(self, product_element) -> str:
        """Get product title from a scoped product element."""
        return product_element.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()

    def get_product_price(self, product_element) -> float:
        """Gets the current active price of a product element."""
        price_text = product_element.locator('.price').inner_text()
        matches    = re.findall(r'\d+\.?\d*', price_text)
        if matches:
            return float(matches[-1])
        return 0.0

    # ── Sale badge helpers ────────────────────────────────────────────────────

    def get_expected_sale_count(self) -> int:
        """
        Count all sale badges on the page before the loop starts.
        Used in the final assertion:
            assert total_processed == get_expected_sale_count()
        """
        return self.page.locator('li.product span.onsale').count()

    def has_sale_badge(self, product_element) -> bool:
        """Return True if a product card has a visible sale badge."""
        sale_badge = product_element.locator('span.onsale')
        return sale_badge.count() > 0 and sale_badge.is_visible()

    def get_sale_discount(self, product_element) -> int:
        """
        Extract the discount % from the sale badge text.
        Badge shows '-25%' or '25%' — returns the integer only.
        Returns 0 if no valid number found.
        """
        sale_badge = product_element.locator('span.onsale')
        sale_text  = sale_badge.inner_text().strip()
        match      = re.search(r'\d+', sale_text)
        return int(match.group()) if match else 0

    # ── Cart actions ──────────────────────────────────────────────────────────

    def add_item_to_cart_by_index(self, index: int) -> str:
        """
        Add a product to cart by its position in the grid.

        Steps:
        1. Scope to the product at the given index
        2. Hover to reveal the hidden Add to Cart button (CSS animation)
        3. Wait for animation to complete
        4. Extract title for tracking
        5. Click the button
        6. Wait for WooCommerce AJAX to finish

        Returns:
            str — product name so the caller can track what was added
        """
        product_list    = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        product_item    = product_list.locator(TeaPageLocators.PRODUCT_ITEM).nth(index)

        product_item.hover()
        self.page.wait_for_timeout(500)

        title_locator   = product_item.locator(TeaPageLocators.PRODUCT_TITLE)
        add_to_cart_btn = product_item.locator(TeaPageLocators.ADD_TO_CART_BTN)

        item_name = title_locator.inner_text()

        self.click_element(add_to_cart_btn)
        self.page.wait_for_timeout(2000)

        return item_name

    # ── Wishlist actions ──────────────────────────────────────────────────────

    def add_item_to_wishlist_by_name(self, tea_name: str) -> bool:
        """
        Add a product to wishlist by its name using human-like mouse movement.

        Why human-like?
        Some bot detection systems watch for instant teleport clicks.
        Moving the mouse across frames (steps=10) looks more natural.

        Returns:
            bool — True if the filled heart icon appeared (confirmed added)
        """
        product_list     = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        specific_product = (
            product_list
            .locator(TeaPageLocators.PRODUCT_ITEM)
            .filter(has_text=tea_name)
            .first
        )
        wishlist_btn = specific_product.locator(TeaPageLocators.ADD_TO_WISHLIST_BTN)

        specific_product.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        box = wishlist_btn.bounding_box()

        if box:
            self.page.mouse.move(
                box["x"] + box["width"] / 2,
                box["y"] + box["height"] / 2,
                steps=10
            )
            self.page.wait_for_timeout(300)
            self.page.mouse.down()
            self.page.wait_for_timeout(150)
            self.page.mouse.up()
        else:
            wishlist_btn.click(delay=150)

        try:
            filled_heart = specific_product.locator('#yith-wcwl-icon-heart')
            filled_heart.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    def add_item_to_wishlist_via_product_page(self, index: int) -> str | None:
        """
        Navigate to the product detail page and add it to the wishlist.

        Why via the product page?
        Some products don't show a wishlist button on the grid card.
        The product page always has it.

        Key improvement over bool return:
        We capture the item name BEFORE navigating away so the caller
        doesn't need to fetch it separately.

        Returns:
            str  — product name if successfully added to wishlist
            None — if wishlist button not found or click failed
        """
        product_list    = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        product_element = product_list.locator(TeaPageLocators.PRODUCT_ITEM).nth(index)

        # Capture name BEFORE navigating away — can't read it after
        item_name = product_element.locator(TeaPageLocators.PRODUCT_TITLE).inner_text()

        title_locator = product_element.locator(TeaPageLocators.PRODUCT_TITLE)
        self.click_element(title_locator)
        self.page.wait_for_load_state("networkidle")

        wishlist_btn = self.page.locator(TeaPageLocators.SINGLE_PRODUCT_WISHLIST_BTN).first

        try:
            wishlist_btn.click(delay=150)
            filled_heart = self.page.locator('#yith-wcwl-icon-heart').first
            filled_heart.wait_for(state="visible", timeout=4000)
            success = True
        except Exception:
            success = False

        self.page.go_back()
        self.page.wait_for_load_state("networkidle")

        return item_name if success else None

    # ── Scrolling ─────────────────────────────────────────────────────────────

    def scroll_to_load_all_products(self) -> int:
        """
        Scroll down using PageDown until no new products load.

        Why needed:
        iTea uses lazy loading — products below the fold are not in
        the DOM until the user scrolls. Without this, the loop only
        sees the first few products.

        Algorithm:
        - Press PageDown and wait for AJAX
        - If product count increased → keep scrolling, reset retries
        - If count unchanged → increment retry counter
        - Stop when retries reach 5 (we are at the bottom)

        Returns:
            int — total number of products loaded into the DOM
        """
        last_count = 0
        retries    = 0

        while retries < 5:
            self.page.keyboard.press("PageDown")
            self.page.wait_for_timeout(1000)

            current_count = self.page.locator(TeaPageLocators.PRODUCT_ITEM).count()

            if current_count > last_count:
                last_count = current_count
                retries    = 0
            else:
                retries += 1

        print(f"--- Finished scrolling! Total products loaded: {last_count} ---")

        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(1000)

        total_products = (
            self.page
            .locator(TeaPageLocators.PRODUCT_LIST)
            .locator(TeaPageLocators.PRODUCT_ITEM)
            .count()
        )

        return total_products

    def re_scroll_to_recover_products(self, total_products: int):
        """
        After navigating to a product page and back, the lazy-loaded
        products disappear from the DOM. Scroll down to recover them.

        Why needed:
        Navigating away and back reloads the category page from scratch.
        Products below the fold vanish until scrolled to again.

        Stops as soon as the expected count is restored.
        """
        for _ in range(25):
            self.page.mouse.wheel(0, 1000)
            self.page.wait_for_timeout(300)

            current_count = self.page.locator(TeaPageLocators.PRODUCT_ITEM).count()

            if current_count >= total_products:
                print(f"   --> Recovered {current_count} items in DOM.")
                break

        self.page.wait_for_timeout(1000)