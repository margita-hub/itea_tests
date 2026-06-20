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


    def click_add_to_cart(self):
        add_to_cart_btn = self.page.locator('button[name="add-to-cart"]')
        if add_to_cart_btn.count() > 0:
            add_to_cart_btn.wait_for(state="visible", timeout=5000)
            add_to_cart_btn.click()
            self.page.wait_for_timeout(500)

            toast = self.page.locator('.woocommerce-message').first
            if toast.count() > 0 and toast.is_visible():
                print(f" Toast: {toast.inner_text()}")
        else:
            add_to_cart_link = self.page.locator('a.add_to_cart_button')
            add_to_cart_link.wait_for(state="visible", timeout=5000)
            add_to_cart_link.click()
            self.page.wait_for_timeout(500)

            toast = self.page.locator('.woocommerce-message').first
            if toast.count() > 0 and toast.is_visible():
                print(f" Toast: {toast.inner_text()}")

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


    def all_product_titles_contain(self, keyword: str) -> bool:
        titles = self.page.locator('li.title.desktop a')
        titles.first.wait_for(state="visible", timeout=5000)
        total = titles.count()
        assert total > 0, "No product titles found on page"
        for i in range(total):
            if keyword.lower() not in titles.nth(i).inner_text().strip().lower():
                return False
        return True

    def extract_price(self, price_text: str) -> float:
        matches = re.findall(r'\d+\.?\d*', price_text)
        if matches:
            return float(matches[-1])
        return 0.0


    def get_sale_products(self) -> list:
        products = self.page.locator('li.product')
        products.first.wait_for(state="visible", timeout=5000)
        total = products.count()
        assert total > 0, "No products found on page"

        sale_items = []
        for i in range(total):
            product = products.nth(i)
            if product.locator('.onsale').is_visible():
                sale_items.append({
                    "index": i,
                    "name": product.locator('.woocommerce-loop-product__title').inner_text(),
                    "price": product.locator('.price').inner_text(),
                })

        print(f"Found {len(sale_items)} sale items out of {total} total")
        return sale_items


    def close_cart_bounce_popup(self):
        close_btn = self.page.locator('#cartbounty-pro-exit-intent-close')
        if close_btn.is_visible():
            close_btn.click()
            self.page.wait_for_timeout(500)

    def is_cart_bounce_popup_visible(self) -> bool:
        popup = self.page.locator('#cartbounty-pro-exit-intent-form-content')
        return popup.is_visible()

    def save_cart_with_email(self, email: str):
        email_input = self.page.locator('#cartbounty-pro-exit-intent-email')
        email_input.wait_for(state="visible", timeout=5000)
        email_input.fill(email)

        save_btn = self.page.locator('#cartbounty-pro-exit-intent-submit')
        save_btn.click()
        self.page.wait_for_timeout(1000)

    def click_and_catch_false_toast(self, button_locator, action_name: str) -> dict:
        print(f" TOAST CATCHER: Clicking '{action_name}'")

        button_locator.wait_for(state="visible", timeout=5000)
        button_locator.click()
        self.page.wait_for_timeout(1000)

        toast = self.page.locator('.woocommerce-message, .wc-bookings-notices, .cart-notice').first
        toast_appeared = toast.is_visible() if toast.count() > 0 else False
        toast_text = toast.inner_text() if toast_appeared else ""

        result = {
            'button_clicked': True,
            'toast_appeared': toast_appeared,
            'toast_text': toast_text,
            'is_false_toast': False
        }

        if toast_appeared:
            print(f"Toast: {toast_text}")

            # Check if toast mentions "added" or "cart"
            if "add" in toast_text.lower() or "cart" in toast_text.lower():
                print(f" Toast claims item was added")
                result['is_false_toast'] = True  # Mark for investigation
        else:
            print(f"No toast message")

        return result


