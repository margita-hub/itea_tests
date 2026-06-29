from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators import LoginPageLocators
from utils.logger import log_message, LogLevel
from config.config import LOGIN_URL
import allure


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_field = self.page.locator(LoginPageLocators.USERNAME_FIELD)
        self.password_field = self.page.locator(LoginPageLocators.PASSWORD_FIELD)
        self.login_button = self.page.locator(LoginPageLocators.LOGIN_BUTTON)
        self.error_message = self.page.locator(LoginPageLocators.ERROR_MESSAGE)

    @allure.step("Load login page")
    def load(self):
        self.navigate_to(LOGIN_URL)

    @allure.step("Get error message")
    def get_error_message(self, expected_error_message):
        return self.error_message.locator(f"//div[contains(text(),'{expected_error_message}')]")

    @allure.step("Perform login with username: {username}")
    def perform_login(self, username: str, password: str):
        log_message(self.logger, "Performing login actions", LogLevel.INFO)
        self.type_text(self.username_field, username)
        self.type_text(self.password_field, password)
        self.click_element(self.login_button)