from playwright.sync_api import expect
import logging
from pages.base_page import BasePage
from utils.logger import LogLevel, take_screenshot, log_message



class AppValidation(BasePage):
    # Inside helper/validation.py __init__
    def __init__(self, **pages):
        self.page = pages.get("page_instance")
        super().__init__(self.page)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.pages = pages
        self.login_page = pages.get("login")
        self.home_page = pages.get("home")

    #def __init__(self,page, setup_all_page):
        #self.login_page, self.home_page = setup_all_page
        #super().__init__(self.login_page)



    def validate_user_logged_in(self):
        login_button = self.login_page.login_button
        try:
            expect(login_button).not_to_be_visible(),"failed to login"
        except Exception as e:
            log_message(self.logger, "login failed",LogLevel.ERROR)
            take_screenshot(self.page,"failed login")
            raise Exception("login failed, the login button still appears") from e


    def validate_user_failed_login(self, expected_error):
        login_button = self.login_page.login_button
        get_error_message = self.login_page.get_error_message

        try:
            expect(login_button).to_be_visible(),"login button was expected to be hidden, but it was visible"
            expect(get_error_message).to_be_visible(),"expected error message mismatch"
        except Exception as e:
            log_message(self.logger, "login button was expected to be hidden, but it was visible",LogLevel.ERROR)
            take_screenshot(self.page,"login button was expected to be hidden, but it was visible")
            raise Exception("login failed: the login button still appears") from e

