from playwright.sync_api import Page

from config.config import WISHLIST_URL
from pages.base_page import BasePage


class WishlistPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def get_wishlist_item_names(self) -> list[str]:
        self.page.locator("td.product-name").first.wait_for(timeout=5000)

        # Get all text from the product names in the wishlist table
        return self.page.locator("td.product-name a").all_inner_texts()


    def load(self):
        self.navigate_to(WISHLIST_URL)
