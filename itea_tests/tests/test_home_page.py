"""
test_home_page.py — tests for the iTea home page.
Uses HomePage to interact with the page — no XPaths or raw Selenium here.
"""

import pytest
from pages.home_page import HomePage



class TestHomePage:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = HomePage(driver)

    # ── Test 1: Logo existence ──────────────────────────────────────────────
    def test_logo_is_displayed(self):
        """Verify the iTea logo exists and is visible."""
        assert self.page.is_logo_visible(), "Logo is NOT visible on the home page"
        
        alt = self.page.get_logo_alt()
        assert alt == "iTea", f"Expected alt='iTea', got '{alt}'"
        
        src = self.page.get_logo_src()
        assert "logo_mobile.png" in src, f"Unexpected logo src: '{src}'"
        
        print(f"\n✅ Logo OK | alt='{alt}' | src='{src}'")

    # ── Test 2: Logo image — MD5 hash comparison ────────────────────────────
    def test_logo_image_hash(self):
        """
        Verifies the logo image file has not changed.
        First run saves the reference. Every run after compares against it.
        """
        current_hash = self.page.compute_logo_md5()
        print(f"\n🔑 Current MD5: {current_hash}")

        if not self.page.reference_hash_exists():
            self.page.save_reference_hash(current_hash)
            pytest.skip("First run — reference hash saved. Re-run to compare.")

        expected_hash = self.page.load_reference_hash()
        print(f"🔑 Expected MD5: {expected_hash}")

        assert current_hash == expected_hash, (
            f"Logo image has CHANGED!\n"
            f"  Expected : {expected_hash}\n"
            f"  Current  : {current_hash}"
        )
        print("✅ Logo image is unchanged")
