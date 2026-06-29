import logging
import pytest
import os
from utils.logger import log_message, take_screenshot, LogLevel
from pages.cart_page import CartPage
from pages.coffee_page import CoffeePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.tea_page import TeaPage
from pages.teawear_page import TeawarePage
from pages.wishlist_page import WishlistPage
from utils.bug_reporter import BugReporter
from pages.product_page import ProductPage

logger = logging.getLogger(__name__)




@pytest.fixture(scope="session")
def browser_instance(request):
    from playwright.sync_api import sync_playwright

    env_headless = os.getenv('HEADLESS', 'false').lower() == 'true'
    cli_headless = request.config.getoption("--headless").lower() == "true"
    headless = env_headless or cli_headless

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()


@pytest.fixture()
def setup_all_page(setup_all_page_session):
    """Uses one session browser ."""
    return setup_all_page_session


@pytest.fixture(autouse=True)
def cleanup_after_test(request):
    yield

    data_changing = ['cart', 'e2e', 'select_options', 'math']
    markers = [m.name for m in request.node.iter_markers()]

    if any(m in markers for m in data_changing):
        try:
            cart = setup_all_page_session["cart"]
            cart.load()
            if cart.count_items() > 0:  # ← only clean if needed!
                cart.remove_all_items()

            wishlist = setup_all_page_session["wishlist"]
            wishlist.load()
            if not wishlist.is_empty():  # ← only clean if needed!
                wishlist.remove_all_items()
        except Exception as e:
            log_message(logger, f"Cleanup failed: {e}", LogLevel.WARNING)


@pytest.fixture(scope="session")
def setup_all_page_session(browser_instance):
    """ONE shared page for read-only tests."""
    context = browser_instance.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    home = HomePage(page)
    home.load()
    home.close_cart_bounce_popup()

    yield {
        "page":     page,
        "home":     home,
        "login":    LoginPage(page),
        "tea":      TeaPage(page),
        "teaware":  TeawarePage(page),
        "cart":     CartPage(page),
        "coffee":   CoffeePage(page),
        "wishlist": WishlistPage(page),
        "product":  ProductPage(page),
    }

    context.close()



@pytest.fixture(autouse=True)
def scroll_to_top(request):
    yield
    if 'setup_all_page_session' in request.fixturenames:
        try:
            session = request.getfixturevalue('setup_all_page_session')
            page = session["page"]
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(300)
        except Exception:
            pass




def _get_page_from_item(item):
    funcargs = getattr(item, "funcargs", {})
    if funcargs.get("setup_playwright") is not None:
        return funcargs["setup_playwright"]
    for fixture in ("setup_all_page", "setup_all_page_session"):
        pages = funcargs.get(fixture)
        if isinstance(pages, dict) and pages.get("page") is not None:
            return pages["page"]
    for name in ("setup_home_page", "setup_login_page"):
        po = funcargs.get(name)
        if po is not None and hasattr(po, "page"):
            return po.page
    return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        test_name = item.name
        clean_error_message = str(call.excinfo.value) if call.excinfo else "Unknown error"
        log_message(logger, f"TEST FAILED: {test_name} -> {clean_error_message}", LogLevel.ERROR)
        page = _get_page_from_item(item)
        if page is not None:
            take_screenshot(page, f"FAILURE_{test_name}")

    if rep.when == "teardown":
        call_rep = getattr(item, "rep_call", None)
        if call_rep and call_rep.failed:
            test_name = item.name
            clean_error_message = str(call_rep.longrepr) if call_rep.longrepr else "Unknown error"
            test_docstring = item.obj.__doc__ or "No steps provided."
            trace_path = getattr(item, "_trace_path", None)
            BugReporter.report_failed_test(test_name, clean_error_message, test_docstring, trace_path)


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run browser headless: true or false",
    )