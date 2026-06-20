
import pytest
import logging
from utils.logger import log_message, LogLevel

logger = logging.getLogger(__name__)


def test_logo_is_displayed(setup_home_page):
    #Verify the iTea logo exists and is visible
    home_page = setup_home_page
    
    assert home_page.is_logo_visible(), "Logo is NOT visible on the home page"
    
    alt = home_page.get_logo_alt()
    assert alt == "iTea", f"Expected alt='iTea', got '{alt}'"
    
    src = home_page.get_logo_src()
    assert "logo_mobile.png" in src, f"Unexpected logo src: '{src}'"
    
    log_message(logger, f"Logo OK | alt='{alt}' | src='{src}'", LogLevel.INFO)


def test_logo_image_hash(setup_home_page):
    # Verifies the logo image file has not changed.First run saves the reference. Every run after compares against it.
    home_page = setup_home_page
    current_hash = home_page.compute_logo_md5()
    log_message(logger, f"Current MD5: {current_hash}", LogLevel.INFO)

    if not home_page.reference_hash_exists():
        home_page.save_reference_hash(current_hash)
        pytest.skip("First run — reference hash saved. Re-run to compare.")

    expected_hash = home_page.load_reference_hash()
    log_message(logger, f"Expected MD5: {expected_hash}", LogLevel.INFO)

    assert current_hash == expected_hash, (
        f"Logo image has CHANGED!\n"
        f"  Expected : {expected_hash}\n"
        f"  Current  : {current_hash}"
    )
    log_message(logger, "Logo image is unchanged", LogLevel.INFO)



@pytest.mark.parametrize("social_network, expected_url", [
    ("instagram", "instagram.com/itea.israel"),
    ("youtube", "youtube.com/user/IteaIsrael"),
    ("facebook", "facebook.com/itea.israel")
])
def test_social_media_links_strictly(setup_all_page, social_network, expected_url):
    home_page = setup_all_page["home"]
    context = home_page.page.context
    home_page.navigate_to("https://itea.co.il/en/")
    home_page.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    social_link = home_page.page.locator(f'#ocean_social-1 ul li a:has(.fa-{social_network})')

    assert social_link.count() > 0
    assert social_link.is_visible()

    with context.expect_page() as new_page_info:
        social_link.click()

    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")
    final_url = new_page.url

    # STRICT ASSERTION!
    # If it hits an error page or login wall, this will immediately fail!
    assert expected_url in final_url, (
        f"Broken Social Link! Clicked {social_network}. \n"
        f"Expected to land on: {expected_url}\n"
        f"Actually landed on: {final_url}"
    )

    new_page.close()
