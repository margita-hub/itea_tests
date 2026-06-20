from pages.locators import LoginPageLocators
from utils.logger import log_message, LogLevel, take_screenshot
from pages.base_page import BasePage
from pages.home_page import HomePage
from playwright.sync_api import Page
from config.config import LOGIN_URL



class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_field = self.page.locator(LoginPageLocators.USERNAME_FIELD)
        self.password_field = self.page.locator(LoginPageLocators.PASSWORD_FIELD)
        self.login_button = self.page.locator(LoginPageLocators.LOGIN_BUTTON)
        self.error_message = self.page.locator(LoginPageLocators.ERROR_MESSAGE) #//*[@id="customer_login"]/div[1]/form/p[3]/div[2]


    def load(self):
        self.navigate_to(LOGIN_URL)


    def get_error_message(self,expected_error_message):
        return self.error_message.locator(f"//div[contains(text(),'{expected_error_message}')]")

    def perform_login(self, username: str, password: str):
        log_message(self.logger, "Performing login actions", LogLevel.INFO)

        self.type_text(self.username_field, username)
        self.type_text(self.password_field, password)
        self.click_element(self.login_button)



    '''
    # if visible here! validation.py should handel it .
    def perform_login(self, username: str, password: str):
        log_message(self.logger, "Performing login", level=LogLevel.INFO)
        self.type_text(self.username_field, username)
        self.type_text(self.password_field, password)
        self.click_element(self.login_button)
        if self.login_button.is_visible():
            log_message(self.logger, "Login failed", level=LogLevel.ERROR)
            take_screenshot(self.page, "login failed")
            return None
        return HomePage(self.page)

'''
'''
       removed -> to not repeat 
    #def verify_login(self): -> validation.py...

    #def verify_login(self):
        try:
        expect(self.login_button).to_be_visible(),"fail tp login"
        expect:
        take_screenshot(self.page, "login failed")

'''