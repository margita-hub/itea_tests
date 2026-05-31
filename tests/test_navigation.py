import pytest
from pages.locators import HomePageLocators

class TestCategoryNavigation:
    
    @pytest.mark.parametrize("menu_locator_name, expected_h1_title", [
        ("TEA_MENU", "Tea"),
        ("TEAWARE_MENU", "Teaware"),
        ("COFFEE_MENU", "Coffee"),
        ("SALE_MENU", "Sale"),
        ("MATCHA_MENU", "Matcha")
    ])
    def test_navigate_to_categories(self, setup_all_page, menu_locator_name, expected_h1_title):
        home_page = setup_all_page["home"]
        
        home_page.navigate_to("https://itea.co.il/en/")
        home_page.page.wait_for_load_state("domcontentloaded")
        
        # --- SPECIAL HANDLING FOR SUB-MENUS ---
        # If Matcha, we have to hover over "Tea Types" to open the dropdown!
        if menu_locator_name == "MATCHA_MENU":
            # We locate the "Tea Types" text and hover over it
            tea_types = home_page.page.locator('text="Tea Types"').first
            tea_types.hover(force=True)
            home_page.page.wait_for_timeout(800) # Wait for dropdown animation to finish
        # --------------------------------------
        
        locator_string = getattr(HomePageLocators, menu_locator_name)
        menu_link = home_page.page.locator(locator_string).first
        
        assert menu_link.is_visible(), f"Could not find the {expected_h1_title} menu link in the header!"
        menu_link.click()
        
        # --- VERIFY NAVIGATION SUCCESS ---
        if menu_locator_name == "SALE_MENU":
            # 1. The Sale page doesn't have an H1, so verify the URL
            home_page.page.wait_for_load_state("domcontentloaded")
            assert "on-sale" in home_page.page.url, "Navigation Bug! Did not land on the Sale page."
            
            # 2. User Suggestion: Verify every item has a sale badge!
            products = home_page.page.locator('li.product')
            products.first.wait_for(state="visible", timeout=5000)
            product_count = products.count()
            
            assert product_count > 0, "Bug: No products found on the Sale page!"
            
            for i in range(product_count):
                product = products.nth(i)
                sale_badge = product.locator('.onsale')
                assert sale_badge.is_visible(), f"Bug! Product at index {i} on Sale page is missing a sale badge!"
                
        elif menu_locator_name == "MATCHA_MENU":
            # 1. Verify H1 title
            h1_element = home_page.page.locator('h1.page-header-title').first
            h1_element.wait_for(state="visible", timeout=5000)
            h1_text = h1_element.inner_text().strip()
            assert expected_h1_title.lower() in h1_text.lower(), (
                f"Navigation Bug! Clicked {expected_h1_title}, but landed on page titled: '{h1_text}'"
            )
            
            # 2. User Suggestion: Verify every item has "matcha" in its title!
            product_titles = home_page.page.locator('li.title.desktop a')
            product_titles.first.wait_for(state="visible", timeout=5000)
            title_count = product_titles.count()
            
            assert title_count > 0, "Bug: No products found on the Matcha page!"
            
            for i in range(title_count):
                title_text = product_titles.nth(i).inner_text().strip()
                assert "matcha" in title_text.lower(), f"Bug! Product '{title_text}' does not contain 'Matcha'!"
                
        else:
            # Verify the H1 title matches for all other pages!
            h1_element = home_page.page.locator('h1.page-header-title').first
            h1_element.wait_for(state="visible", timeout=5000)
            h1_text = h1_element.inner_text().strip()
            
            assert expected_h1_title.lower() in h1_text.lower(), (
                f"Navigation Bug! Clicked {expected_h1_title}, but landed on page titled: '{h1_text}'"
            )
