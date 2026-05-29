from playwright.sync_api import Page
from pages.base_page import BasePage



from playwright.sync_api import Page
from pages.base_page import BasePage


class TeaPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)


#class TeaPageLocators:
    #PAGE_TITLE = (By.CSS_SELECTOR, "h1")

# main > header > div > h1

#class TeaPage(BasePage):
    #def __init__(self, driver):
        #super().__init__(driver)

    #def is_page_loaded(self) -> bool:
        #return self.is_element_visible(TeaPageLocators.PAGE_TITLE)

    #def get_title_text(self) -> str:
        #element = self.find_element(TeaPageLocators.PAGE_TITLE)
        #return element.text