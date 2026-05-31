import pytest
import re
from pages.locators import TeaPageLocators

class TestFilteringAndSorting:

    @pytest.mark.parametrize("top_menu, sub_menu, item, expected_url, expected_h1", [
        ("Choose tea", "Feelings", "relaxation", "teas-for-emotional-wellness-and-relaxation", "emotional wellness and relaxation"),
        ("Choose tea", "Feelings", "energy boost", "energy-booster", "energy levels"),
        ("Choose tea", "Flavors", "fruity", "fruity", "fruity"),
        ("Choose tea", "Time for Tea", "afternoon & evening tea", "time/evening", "evening"),
        ("Choose tea", "Tea & Health", "digestive health", "digestive-health", "digestive health")
    ])
    def test_advanced_dropdown_navigation(self, setup_all_page, top_menu, sub_menu, item, expected_url, expected_h1):
        """Test the multi-level hover menus dynamically for any combination!"""
        home_page = setup_all_page["home"]
        page = home_page.page
        
        home_page.navigate_to("https://itea.co.il/en/")
        page.wait_for_load_state("domcontentloaded")
        
        # 1. Hover over Top Menu
        try:
            page.locator(f'text="{top_menu}"').first.hover(force=True, timeout=2000)
            page.wait_for_timeout(500)
            
            # 2. Hover over Sub Menu
            page.locator(f'text="{sub_menu}"').first.hover(force=True, timeout=2000)
            page.wait_for_timeout(500)
        except:
            pass # If hover fails due to flakiness, we will force click via evaluate below anyway
        
        # 3. Click the target item using force=True to bypass any animation overlaps
        page.locator(f'text="{item}"').first.click(force=True)
        page.wait_for_load_state("domcontentloaded")
        
        # 4. Verify URL and H1 title dynamically
        assert expected_url in page.url, f"Navigation bug! Expected URL to contain '{expected_url}'"
        
        h1_element = page.locator(TeaPageLocators.PAGE_TITLE_H1).first
        h1_element.wait_for(state="visible", timeout=5000)
        h1_text = h1_element.inner_text().strip()
        
        assert expected_h1.lower() in h1_text.lower(), f"Unexpected H1 text: {h1_text}"

    @pytest.mark.parametrize("sort_value, reverse_order", [
        ("price", False),        # Sort by price: low to high
        ("price-desc", True)     # Sort by price: high to low
    ])
    def test_sort_by_price(self, setup_all_page, sort_value, reverse_order):
        """Test that sorting products by price works correctly in both directions"""
        home_page = setup_all_page["home"]
        page = home_page.page
        
        # Go to the main Tea page
        home_page.navigate_to("https://itea.co.il/en/tea/")
        page.wait_for_load_state("domcontentloaded")
        
        # Select sort option from the dropdown
        page.locator(TeaPageLocators.SORTING_DROPDOWN).first.select_option(sort_value)
        page.wait_for_load_state("networkidle")
        
        # Get all product prices on the first page
        price_elements = page.locator(TeaPageLocators.PRODUCT_PRICE).all()
        
        prices = []
        for element in price_elements:
            price_text = element.inner_text()
            # If item is on sale, it has two prices. We take the last one (the actual sale price)
            amounts = re.findall(r'\d+\.\d+|\d+', price_text)
            if amounts:
                prices.append(float(amounts[-1]))
        
        assert len(prices) > 0, "No prices found on the page to sort!"
        
        # Verify the list is sorted correctly based on the expected order
        sorted_prices = sorted(prices, reverse=reverse_order)
        assert prices == sorted_prices, f"Products are not sorted correctly! Found prices: {prices}"
