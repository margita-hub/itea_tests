from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators import TeaPageLocators
import re



class TeaPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def is_page_loaded(self) -> bool:
        # Use the same exact class you found earlier!
        title_locator = self.page.locator('h1.page-header-title')

        try:
            title_locator.wait_for(state="visible", timeout=5000)
            return "Tea" in title_locator.inner_text()
        except Exception:
            return False

    def add_item_to_cart_by_index(self, index: int) -> str:
        # Get the main list
        product_list = self.page.locator(TeaPageLocators.PRODUCT_LIST)

        # Scope to the specific product index
        product_item = product_list.locator(TeaPageLocators.PRODUCT_ITEM).nth(index)

        # Hover over the product so the "Add to Cart" button appears!
        product_item.hover()

        # Wait just a tiny fraction of a second for the CSS animation to show the button
        self.page.wait_for_timeout(500)

        # Find the title and button inside that product
        title_locator = product_item.locator(TeaPageLocators.PRODUCT_TITLE)
        add_to_cart_btn = product_item.locator(TeaPageLocators.ADD_TO_CART_BTN)

        # Extract the name
        item_name = title_locator.inner_text()

        # Click the button
        self.click_element(add_to_cart_btn)

        # Wait for WooCommerce AJAX to finish adding to cart
        self.page.wait_for_timeout(2000)

        return item_name

    def add_item_to_wishlist_by_name(self, tea_name: str) -> bool:
        product_list = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        specific_product = product_list.locator(TeaPageLocators.PRODUCT_ITEM).filter(has_text=tea_name).first
        wishlist_btn = specific_product.locator(TeaPageLocators.ADD_TO_WISHLIST_BTN)

        # 1. Teleport the screen so the product is visible (Bots do this, it's fine)
        specific_product.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # --- HUMAN-LIKE HOVER AND CLICK ---

        # 2. Get the exact X and Y coordinates of the heart button
        box = wishlist_btn.bounding_box()

        if box:
            # 3. Slowly move the mouse to the center of the heart button!
            # The steps=10 makes it drag the mouse across the screen over 10 frames
            self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=10)
            self.page.wait_for_timeout(300)  # Pause before clicking

            # 4. Click the mouse right where it is hovering!
            self.page.mouse.down()
            self.page.wait_for_timeout(150)  # Hold click
            self.page.mouse.up()
        else:
            # Fallback if bounding_box fails for some reason
            wishlist_btn.click(delay=150)

        # ---------------------------

        try:
            filled_heart = specific_product.locator('#yith-wcwl-icon-heart')
            filled_heart.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False


    def add_item_to_wishlist_via_product_page(self, index: int) -> bool:
        # Re-fetch the fresh product list
        product_list = self.page.locator(TeaPageLocators.PRODUCT_LIST)
        product_element = product_list.locator(TeaPageLocators.PRODUCT_ITEM).nth(index)
        
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

        return success

    def get_product_price(self, product_element) -> float:
        """Gets the current active price of a product element."""
        price_text = product_element.locator('.price').inner_text()
        matches = re.findall(r'\d+\.?\d*', price_text)
        if matches:
            return float(matches[-1])
        return 0.0


