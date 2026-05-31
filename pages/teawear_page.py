from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators import TeawarePageLocators


class TeawarePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def is_page_loaded(self) -> bool:
        # Locate the page title
        title_locator = self.page.locator(TeawarePageLocators.PAGE_TITLE)

        try:
            # Wait for it to be visible
            title_locator.wait_for(state="visible", timeout=5000)

            # Verify the text actually says "Teaware"
            return "Teaware" in title_locator.inner_text()
        except Exception:
            return False