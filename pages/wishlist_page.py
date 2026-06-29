from playwright.sync_api import Page
from config.config import WISHLIST_URL
from pages.base_page import BasePage
import allure


class WishlistPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Load wishlist page")
    def load(self):
        self.navigate_to(WISHLIST_URL)

    @allure.step("Get wishlist item names")
    def get_wishlist_item_names(self) -> list[str]:
        self.page.locator("td.product-name").first.wait_for(timeout=5000)
        return self.page.locator("td.product-name a").all_inner_texts()

    @allure.step("Check wishlist is empty")
    def is_empty(self) -> bool:
        return self.page.locator("td.product-name").count() == 0

    @allure.step("Remove all items from wishlist")
    def remove_all_items(self):
        self.load()
        while not self.is_empty():
            self.page.locator("td.product-remove a").first.click()
            self.page.wait_for_timeout(500)