from config.config import TEAWARE_URL
from pages.locators import TeaPageLocators


class TestTeawarePage:

    def load(self):
        self.navigate_to(TEAWARE_URL)

    def test_teaware_page_loads_correctly(self, setup_all_page):
        teaware_page = setup_all_page["teaware"]
        teaware_page.load()
        assert teaware_page.is_page_loaded(), "Teaware page title is NOT visible!"
        count = teaware_page.page.locator(TeaPageLocators.PRODUCT_ITEM).count()
        assert count > 0, "Teaware page loaded but shows zero products!"

