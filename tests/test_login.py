import pytest

from config.config import VALID_CREDENTIALS
#from pages.base_page import browser
#from pages.login_page import LoginPage
from config.config import VALID_CREDENTIALS

import pytest

@pytest.mark.skip(reason="Cloudflare Captcha currently blocking login flow")
class TestLogin:
# open browser and load the login page
    def test_success_login_page(self,setup_load_page, validation):
        login_page = setup_load_page
        login_page.perform_login(VALID_CREDENTIALS["email"], VALID_CREDENTIALS["password"])
        validation.validate_user_logged_in()

    def test_user_can_navigate_and_login(self, setup_all_page, validation):
        # setup_all_page gives us a dictionary of all our pages!
        home_page = setup_all_page["home"]
        login_page = setup_all_page["login"]

        # 1. Start at the Home Page
        home_page.navigate_to("https://itea.co.il/en/")

        # 2. Click the Login Icon (Takes us to Login Page)
        home_page.click_login_icon()

        # 3. Now we use the LoginPage object to login!
        login_page.perform_login(VALID_CREDENTIALS["email"], VALID_CREDENTIALS["password"])

        # 4. Verify Success
        validation.validate_user_logged_in()


    @pytest.mark.parametrize("username, password, error_message",
                             [
                                 ("wrong_username", "valid_password", "Unknown email address. Check again or try your username."),
                                 ("valid_username", "wrong_password","The password you entered is incorrect"),
                                 ("", "valid_password", "Please fill all required fields"),
                                 ("valid_username", "", "Please fill all required fields"),
                             ])
    def test_failed_login(self,setup_load_page, validation, username, password, error_message):
        login_page = setup_load_page
        login_page.perform_login(username, password)
        validation.validate_user_failed_login(error_message)




#login_button = login_page.login_button
    #expect(login_button).to_be_visible(), "fail to login"
   #browser = playwright.chromium.launch(headless=False)
    #page = browser.new_page()
    #page.navigateTo(URL)

# username
# password
# press Login
# verify logged in successfully



#test 2
# [wrong username, valid password]
# [ valid username, wrong password]
# [ missing username, valid password]
# [ valid username, missing password]
# open browser and load the login page
# enter test case
#press Login


# verify failed login