import pytest


class TestTeawarePage:
    def test_teaware_page_loads_correctly(self, setup_all_page):
        # Grab the TeawarePage object from your universal fixture
        # (Make sure the key matches exactly what you put in conftest.py)
        teaware_page = setup_all_page["teaware"]

        # Navigate using your custom BasePage method
        teaware_page.navigate_to("https://itea.co.il/en/teaware/")

        # Assert it loaded!
        assert teaware_page.is_page_loaded(), "Teaware page title is NOT visible!"

