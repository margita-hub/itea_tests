import pytest
from config.config import VALID_CREDENTIALS

pytestmark = pytest.mark.login


@pytest.mark.skip(reason="Cloudflare Captcha currently blocking login flow")
class TestLogin:
    def test_success_login_page(self, setup_login_page, validation):
        login_page = setup_login_page
        login_page.perform_login(VALID_CREDENTIALS["email"], VALID_CREDENTIALS["password"])
        validation.validate_user_logged_in()

    def test_user_can_navigate_and_login(self, setup_all_page, validation):
        login_page = setup_all_page["login"]
        login_page.load()
        login_page.login_with_valid_credentials()

    @pytest.mark.parametrize("username, password, error_message", [
        ("wrong_username", "valid_password", "Unknown email address. Check again or try your username."),
        ("valid_username", "wrong_password", "The password you entered is incorrect"),
        ("", "valid_password", "Please fill all required fields"),
        ("valid_username", "", "Please fill all required fields"),
    ])
    def test_failed_login(self, setup_login_page, validation, username, password, error_message):
        login_page = setup_login_page
        login_page.perform_login(username, password)
        validation.validate_user_failed_login(error_message)