import pytest
from pages.tea_page import TeaPage


pytestmark = pytest.mark.tea
class TestTeaPage:
    def test_tea_page_loads_correctly(self, setup_all_page_session):
        home_page = setup_all_page_session["home"]
        tea_page = setup_all_page_session["tea"]
        home_page.click_tea_menu()
        assert tea_page.is_page_loaded(), "Tea page title is NOT visible!"

