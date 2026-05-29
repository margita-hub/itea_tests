import pytest

from config.config import VALID_CREDENTIALS
#from pages.base_page import browser
#from pages.login_page import LoginPage


# open browser and load the login page
def test_success_login_page(setup_load_page, validation):
    login_page = setup_load_page
    login_page.perform_login(VALID_CREDENTIALS["email"], VALID_CREDENTIALS["password"])
    validation.validate_user_logged_in()


@pytest.mark.parametrize("username, password, error_message",
                         [
                             ("wrong_username", "valid_password", "Unknown email address. Check again or try your username."),
                             ("valid_username", "wrong_password","The password you entered is incorrect"),
                             ("", "valid_password", "Please fill all required fields"),
                             ("valid_username", "", "Please fill all required fields"),
                         ])
def test_failed_login(setup_load_page, validation, username, password, error_message):
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