import pytest
import pytest_check as check
from pages.locators import TeaPageLocators

pytestmark = pytest.mark.teaware


class TestTeawarePage:
    def test_teaware_page_loads_correctly(self, setup_all_page_session):
        """Teaware page loads with correct title and products."""
        teaware_page = setup_all_page_session["teaware"]

        teaware_page.load()
        teaware_page.page.wait_for_load_state("domcontentloaded")

        check.is_true(teaware_page.is_page_loaded(), "Teaware page title is NOT visible!")
        count = teaware_page.page.locator(TeaPageLocators.PRODUCT_ITEM).count()
        check.greater(count, 0, "Teaware page loaded but shows zero products!")