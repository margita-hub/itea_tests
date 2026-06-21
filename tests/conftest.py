import logging
import pytest
import time
import threading
import sys
import os
from pathlib import Path
from utils.logger import log_message, take_screenshot, LogLevel
from config.config import URL_EN, LOGIN_URL
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


@pytest.fixture()
def setup_playwright(playwright, request):
    # Check environment variable first (for CI), then command-line option
    env_headless = os.getenv('HEADLESS', 'false').lower() == 'true'
    cli_headless = request.config.getoption("--headless").lower() == "true"
    headless = env_headless or cli_headless

    browser = playwright.chromium.launch(headless=headless)

    # handle for tracing -> Starts Playwright Tracing to record a "black box" video/network log of the test. The try/finally block below ensures we only save the heavy .zip file if the test actually fails.
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    log_message(logger, "Browser opened", LogLevel.INFO)

    try:
        yield page  # tests are unchanged — still get a page
    finally:
        failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
        if failed:
            test_name = request.node.name.replace("[", "-").replace("]", "")
            timestamp = time.strftime("%m%d-%H%M%S")
            Path("traces").mkdir(exist_ok=True)
            context.tracing.stop(path=f"traces/trace_{test_name}_{timestamp}.zip")
        else:
            context.tracing.stop()  # discard cleanly -> stops

        log_message(logger, "Browser closing", LogLevel.INFO)
        browser.close()

@pytest.fixture()
def setup_home_page(setup_playwright):
    home_page = HomePage(setup_playwright)
    home_page.load()
    log_message(logger, f"Navigated to {URL_EN}", LogLevel.INFO)
    yield home_page


@pytest.fixture()
def setup_login_page(setup_playwright):
    login_page = LoginPage(setup_playwright)
    login_page.load()
    log_message(logger, f"Navigated to {LOGIN_URL}", LogLevel.INFO)
    yield login_page


@pytest.fixture()
def setup_all_page(setup_playwright):
    home = HomePage(setup_playwright)
    home.load()
    log_message(logger, f"Navigated to {URL_EN}", LogLevel.INFO)
    home.close_cart_bounce_popup()

    return {
        "page":     setup_playwright,
        "home":     home,
        "login":    LoginPage(setup_playwright),
        "tea":      TeaPage(setup_playwright),
        "teaware":  TeawarePage(setup_playwright),
        "cart":     CartPage(setup_playwright),
        "coffee":   CoffeePage(setup_playwright),
        "wishlist": WishlistPage(setup_playwright),
        "product": ProductPage(setup_playwright),
    }


def _get_page_from_item(item):
    funcargs = getattr(item, "funcargs", {})
    if funcargs.get("setup_playwright") is not None:
        return funcargs["setup_playwright"]
    all_pages = funcargs.get("setup_all_page")
    if isinstance(all_pages, dict) and all_pages.get("page") is not None:
        return all_pages["page"]
    for name in ("setup_home_page", "setup_login_page"):
        po = funcargs.get(name)
        if po is not None and hasattr(po, "page"):
            return po.page
    return None


# this is decorator @pytest.hookimpl and there is function that on test failure pytest stops the test and prints an error in console. to avoid adding try/expect in each test, the Hook is global and its watches all test cases.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)

    # Failure log + screenshot only
    if rep.when == "call" and rep.failed:
        test_name = item.name
        clean_error_message = str(call.excinfo.value) if call.excinfo else "Unknown error"

        log_message(logger, f"TEST FAILED: {test_name} -> {clean_error_message}", LogLevel.ERROR)

        page = _get_page_from_item(item)
        if page is not None:
            take_screenshot(page, f"FAILURE_{test_name}")

    # trace zip exists now, safe to email
    if rep.when == "teardown":
        call_rep = getattr(item, "rep_call", None)
        if call_rep and call_rep.failed:
            test_name           = item.name
            clean_error_message = str(call_rep.longrepr) if call_rep.longrepr else "Unknown error"
            test_docstring      = item.obj.__doc__ or "No steps provided."
            trace_path          = getattr(item, "_trace_path", None)

            BugReporter.report_failed_test(test_name, clean_error_message, test_docstring, trace_path)


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run browser headless: true or false",
    )
    parser.addoption(
        "--no-sleep-prevention",
        action="store_true",
        default=False,
        help="Disable sleep prevention during tests (useful for CI/CD)"
    )



def pytest_configure(config):
    if os.getenv('CI') != 'true':
        if not config.getoption("--no-sleep-prevention"):
            sleep_thread = threading.Thread(target=prevent_sleep, daemon=True)
            sleep_thread.start()
            print("Local machine - Sleep prevention enabled")
    else:
        print(" CI environment - Sleep prevention disabled")



