import pytest
from pages import TeaPage
#from pages.tea_page import TeaPageLocators

class TestTeaPage:
    @pytest.fixture
    def setup(self, driver):
        self.driver = driver
        self.driver.get("https://itea.co.il/en/teaware/")
        self.page = TeaPage(driver)

    def test_teaware_page_loads_correctly(self):
        assert self.page.is_page_loaded(), "Teaware page title is NOT visible!"

