from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def get_cart_item_names(self) -> list[str]:
        # Wait for the cart table to load
        self.page.locator("td.product-name").first.wait_for(timeout=5000) # locator from html-> <td class="product-name" data-title="Product"><a href="https://itea.co.il/en/white/baimudan2/">Bai Mudan (high grade)</a>        <script>...</script></td>


        # Get all the text from the product names in the cart
        return self.page.locator("td.product-name a").all_inner_texts()

    def get_cart_total(self) -> float:
        # Wait for the total to load
        self.page.locator("tr.order-total .woocommerce-Price-amount").wait_for(timeout=5000)

        # Get the text (e.g., "₪ 44.00")
        total_text = self.page.locator("tr.order-total .woocommerce-Price-amount").inner_text()

        # Clean it up to turn it into a number (remove the currency symbol and spaces)
        clean_text = total_text.replace("₪", "").replace(",", "").strip()

        return float(clean_text)