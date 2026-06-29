import pytest
import pytest_check as check

pytestmark = pytest.mark.tea


class TestTeaPage:
    def test_tea_page_loads_correctly(self, setup_all_page_session):
        """Tea page loads with correct title."""
        home_page = setup_all_page_session["home"]
        tea_page = setup_all_page_session["tea"]

        home_page.click_tea_menu()
        check.is_true(tea_page.is_page_loaded(), "Tea page title is NOT visible!")