import pytest
from pages.tea_page import TeaPage


class TestTeaPage:
    def test_tea_page_loads_correctly(self, setup_all_page):
        # 1. Grab the TeaPage object from your fixture
        tea_page = setup_all_page["tea"]

        # 2. Navigate to the TEA page
        tea_page.navigate_to("https://itea.co.il/en/tea/")

        # 3. Assert it loaded!
        assert tea_page.is_page_loaded(), "Tea page title is NOT visible!"

