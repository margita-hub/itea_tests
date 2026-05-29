import pytest
from venv import logger

from config.config import URLEn, URLHe, URLRu, URLLogin
from utils.validation import AppValidation
from pages.cart_page import CartPage
from pages.coffee_page import CoffeePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
#from pages.tea_page import TeaPage
from utils.logger import log_message, LogLevel
from pages.tea_page import TeaPage
from pages.teawear_page import TeawarePage


@pytest.fixture()
def setup_playwright(playwright, request):
    headed = request.config.getoption("--headless", default = "False")
    browser = playwright.chromium.launch(headless = not headed)
    page = browser.new_page()
    try:
        yield page
    finally:
        log_message(logger,"closing browser", LogLevel.INFO)
        browser.close()


@pytest.fixture()
def setup_home_page(setup_playwright):
    home_page = HomePage(setup_playwright)
    home_page.navigate_to(URLLogin)
    log_message(logger, "navigate to{URL}", LogLevel.INFO)
    yield home_page


@pytest.fixture()
def setup_load_page(setup_playwright):
    login_page = LoginPage(setup_playwright)
    login_page.navigate_to(URLLogin)
    log_message(logger, "navigate to{URL}", LogLevel.INFO)
    yield login_page


@pytest.fixture()
def setup_all_page(setup_playwright):
    return {
        "page_instance": setup_playwright,
        "login": LoginPage(setup_playwright),
        "home": HomePage(setup_playwright),
        "teaware": TeawarePage(setup_playwright),
        "cart": CartPage(setup_playwright),
        "coffee": CoffeePage(setup_playwright),
        "tea": TeaPage(setup_playwright)
    }



@pytest.fixture()
def validation(setup_all_page):
    yield AppValidation(**setup_all_page)






'''
from playwright.sync_api import sync_playwright, Page
from pages.home_page import HomePage
from pages.tea_page import TeaPage

BASE_URL = "https://itea.co.il/"

@pytest.fixture(scope="session")
def playwright_instance():
    """Keeps the Playwright process running for the entire test run session."""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="class")
def page(playwright_instance):
    """Provides a single browser tab per test class without forcing early navigation."""
    # Launch browser (set headless=True when running on GitHub Actions CI)
    browser = playwright_instance.chromium.launch(headless=False)

    # Create an isolated context with your standard window viewport size
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    yield page

    browser.close()

@pytest.fixture(scope="function")
def home_page(page: Page):
    """Instantly injects an initialized HomePage instance into your tests."""
    return HomePage(page)

@pytest.fixture(scope="function")
def tea_page(page: Page):
    """Instantly injects an initialized TeaPage instance into your tests."""
    return TeaPage(page)
'''