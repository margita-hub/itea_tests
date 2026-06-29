import pytest
import allure
import logging
import pytest_check as check
from utils.logger import log_message, LogLevel

logger = logging.getLogger(__name__)
pytestmark = pytest.mark.home


@allure.title("Logo is displayed on home page")
@allure.description("Verify iTea logo exists, is visible, has correct alt text and src")
def test_logo_is_displayed(setup_all_page_session):
    """Verify the iTea logo exists and is visible."""
    home_page = setup_all_page_session["home"]

    with allure.step("Navigate to home page"):
        home_page.navigate_to("https://itea.co.il/en/")

    with allure.step("Check logo is visible"):
        check.is_true(home_page.is_logo_visible(), "Logo is NOT visible on the home page")

    with allure.step("Check logo alt text = 'iTea'"):
        alt = home_page.get_logo_alt()
        check.equal(alt, "iTea", f"Expected alt='iTea', got '{alt}'")

    with allure.step("Check logo src contains 'logo_mobile.png'"):
        src = home_page.get_logo_src()
        check.is_in("logo_mobile.png", src, f"Unexpected logo src: '{src}'")

    log_message(logger, f"Logo OK | alt='{alt}' | src='{src}'", LogLevel.INFO)


@allure.title("Logo image hash has not changed")
@allure.description("Verifies logo image file has not changed using MD5 hash comparison")
def test_logo_image_hash(setup_all_page_session):
    """Verifies the logo image file has not changed."""
    home_page = setup_all_page_session["home"]

    with allure.step("Navigate to home page"):
        home_page.navigate_to("https://itea.co.il/en/")

    with allure.step("Compute current logo MD5 hash"):
        current_hash = home_page.compute_logo_md5()
        log_message(logger, f"Current MD5: {current_hash}", LogLevel.INFO)

    with allure.step("Check if reference hash exists"):
        if not home_page.reference_hash_exists():
            home_page.save_reference_hash(current_hash)
            pytest.skip("First run — reference hash saved. Re-run to compare.")

    with allure.step("Compare current hash with reference"):
        expected_hash = home_page.load_reference_hash()
        log_message(logger, f"Expected MD5: {expected_hash}", LogLevel.INFO)
        check.equal(current_hash, expected_hash,
            f"Logo image CHANGED!\n Expected: {expected_hash}\n Current: {current_hash}")

    log_message(logger, "Logo image is unchanged", LogLevel.INFO)


@allure.title("Social media link: {social_network}")
@allure.description("Verify social media links open correct pages")
@pytest.mark.parametrize("social_network, expected_url", [
    ("instagram", "instagram.com/itea.israel"),
    ("youtube", "youtube.com/user/IteaIsrael"),
    ("facebook", "facebook.com/itea.israel")
])
def test_social_media_links_strictly(setup_all_page_session, social_network, expected_url):
    home_page = setup_all_page_session["home"]
    context = home_page.page.context

    with allure.step("Navigate to home page"):
        home_page.click_logo()

    with allure.step("Scroll to footer"):
        home_page.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    with allure.step(f"Find {social_network} link"):
        social_link = home_page.page.locator(f'#ocean_social-1 ul li a:has(.fa-{social_network})')
        check.greater(social_link.count(), 0, f"{social_network} link not found!")
        check.is_true(social_link.is_visible(), f"{social_network} link not visible!")

    with allure.step(f"Click {social_network} and wait for new page"):
        with context.expect_page() as new_page_info:
            social_link.click()
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")

    with allure.step(f"Verify URL contains '{expected_url}'"):
        final_url = new_page.url
        check.is_in(expected_url, final_url,
            f"Broken link! Clicked {social_network}.\nExpected: {expected_url}\nGot: {final_url}")
        new_page.close()