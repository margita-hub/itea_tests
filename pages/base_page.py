import logging
import re
from playwright.sync_api import Page, Locator
from utils.logger import LogLevel, log_message, take_screenshot


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def safe_execute(self, action, action_name: str, *args):
        try:
            log_message(self.logger, f"Execution Action {action_name} with arguments {args}", LogLevel.INFO)
            action(*args)
        except Exception as e:
            log_message(self.logger, f"Action Failed {action_name} with arguments {args}", LogLevel.ERROR)
            take_screenshot(self.page, action_name)
            raise

    def click_element(self, locator: Locator):
        self.safe_execute(locator.click, "click_element")

    def type_text(self, locator: Locator, text: str):
        self.safe_execute(locator.fill, "type_text", text)

    def navigate_to(self, url: str):
        self.safe_execute(self.page.goto,"navigate_to", url)

    def get_page_heading(self) -> str:
        h1 = self.page.locator('h1.page-header-title').first
        h1.wait_for(state="visible", timeout=5000)
        return h1.inner_text().strip().lower()

    def products_missing_sale_badge(self) -> list[str]:
        products = self.page.locator('li.product')
        products.first.wait_for(state="visible", timeout=5000)
        total = products.count()
        assert total > 0, "No products found on page"
        missing = []
        for i in range(total):
            product = products.nth(i)
            if not product.locator('.onsale').is_visible():
                missing.append(product.locator('li.title.desktop a').inner_text().strip())
        return missing

    def products_not_containing(self, keyword: str) -> list[str]:
        titles = self.page.locator('li.title.desktop a')
        titles.first.wait_for(state="visible", timeout=5000)
        total = titles.count()
        assert total > 0, "No product titles found on page"
        bad = []
        for i in range(total):
            text = titles.nth(i).inner_text().strip()
            if keyword.lower() not in text.lower():
                bad.append(text)
        return bad

    def extract_price(self, price_text: str) -> float:
        matches = re.findall(r'\d+\.?\d*', price_text)
        if matches:
            return float(matches[-1])
        return 0.0