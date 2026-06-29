from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators import TeawarePageLocators
from config.config import TEAWARE_URL
import allure


class TeawarePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Load teaware page")
    def load(self):
        self.navigate_to(TEAWARE_URL)

    @allure.step("Check teaware page loaded")
    def is_page_loaded(self) -> bool:
        title_locator = self.page.locator(TeawarePageLocators.PAGE_TITLE)
        try:
            title_locator.wait_for(state="visible", timeout=5000)
            return "Teaware" in title_locator.inner_text()
        except Exception:
            return False