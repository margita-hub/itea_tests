import pytest
import re
import pytest_check as check
from pages.locators import TeaPageLocators

pytestmark = pytest.mark.filtering


class TestFilteringAndSorting:

    @pytest.mark.parametrize("top_menu, sub_menu, item, expected_url, expected_h1", [
        pytest.param("Choose tea", "Feelings", "relaxation", "teas-for-emotional-wellness-and-relaxation", "emotional wellness and relaxation", id="Feelings-relaxation"),
        pytest.param("Choose tea", "Feelings", "energy boost", "energy-booster", "energy levels", id="Feelings-energy-boost"),
        pytest.param("Choose tea", "Flavors", "fruity", "fruity", "fruity", id="Flavors-fruity"),
        pytest.param("Choose tea", "Time for Tea", "afternoon & evening tea", "time/evening", "evening", id="Time-evening"),
        pytest.param("Choose tea", "Tea & Health", "digestive health", "digestive-health", "digestive health", id="Health-digestive"),
    ])
    def test_advanced_dropdown_navigation(self, setup_all_page_session, top_menu, sub_menu, item, expected_url, expected_h1):
        """Test multi-level hover menus for any combination."""
        home_page = setup_all_page_session["home"]
        page = home_page.page

        home_page.click_tea_menu()
        page.wait_for_load_state("domcontentloaded")

        try:
            page.locator(f'text="{top_menu}"').first.hover(force=True, timeout=2000)
            page.wait_for_timeout(500)
            page.locator(f'text="{sub_menu}"').first.hover(force=True, timeout=2000)
            page.wait_for_timeout(500)
        except Exception as e:
            print(f"Hover skipped ({top_menu} → {sub_menu}): {e}")

        page.locator(f'text="{item}"').first.click(force=True)
        page.wait_for_load_state("domcontentloaded")

        check.is_in(expected_url, page.url, f"Navigation bug! Expected URL to contain '{expected_url}'")

        h1_element = page.locator(TeaPageLocators.PAGE_TITLE_H1).first
        h1_element.wait_for(state="visible", timeout=5000)
        h1_text = h1_element.inner_text().strip()
        check.is_in(expected_h1.lower(), h1_text.lower(), f"Unexpected H1 text: {h1_text}")


    @pytest.mark.parametrize("sort_value, reverse_order", [
        ("price", False),
        ("price-desc", True)
    ])
    def test_sort_by_price(self, setup_all_page_session, sort_value, reverse_order):
        """Test sorting products by price works in both directions."""
        home_page = setup_all_page_session["home"]
        page = home_page.page

        home_page.click_tea_menu()
        page.wait_for_load_state("domcontentloaded")

        page.locator(TeaPageLocators.SORTING_DROPDOWN).first.select_option(sort_value)
        page.wait_for_load_state("networkidle")

        price_elements = page.locator(TeaPageLocators.PRODUCT_PRICE).all()
        prices = []
        for element in price_elements:
            price_text = element.inner_text()
            amounts = re.findall(r'\d+\.\d+|\d+', price_text)
            if amounts:
                prices.append(float(amounts[-1]))

        check.greater(len(prices), 0, "No prices found on the page to sort!")
        sorted_prices = sorted(prices, reverse=reverse_order)
        check.equal(prices, sorted_prices, f"Products not sorted correctly! Found: {prices}")