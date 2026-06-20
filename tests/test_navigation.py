import pytest


class TestCategoryNavigation:

    @pytest.mark.parametrize("menu_locator_name, expected_h1_title", [
        pytest.param("TEA_MENU",     "Tea",     id="TEA_MENU-Tea"),
        pytest.param("TEAWARE_MENU", "Teaware", id="TEAWARE_MENU-Teaware"),
        pytest.param("COFFEE_MENU",  "Coffee",  id="COFFEE_MENU-Coffee"),
        pytest.param("SALE_MENU",    "Sale",    id="SALE_MENU-Sale"),
        pytest.param("MATCHA_MENU",  "Matcha",  id="MATCHA_MENU-Matcha"),
    ])
    def test_navigate_to_categories(self, setup_all_page, menu_locator_name, expected_h1_title):
        """Click each header category and verify it lands on the right page."""
        home_page = setup_all_page["home"]
        home_page.load()
        home_page.page.wait_for_load_state("domcontentloaded")

        if menu_locator_name == "MATCHA_MENU":
            home_page.hover_tea_types_menu()

        home_page.click_menu(menu_locator_name)
        home_page.page.wait_for_load_state("domcontentloaded")

        if menu_locator_name == "SALE_MENU":
            assert "on-sale" in home_page.page.url, "Navigation bug — did not land on Sale page"
            missing = home_page.products_missing_sale_badge()
            assert not missing, f"Products missing sale badge: {missing}"

        elif menu_locator_name == "MATCHA_MENU":
            heading = home_page.get_page_heading()
            assert expected_h1_title.lower() in heading, \
                f"Navigation bug — expected '{expected_h1_title}', got '{heading}'"
            bad = home_page.products_not_containing("matcha")
            assert not bad, f"Products not containing 'matcha': {bad}"

        else:
            heading = home_page.get_page_heading()
            assert expected_h1_title.lower() in heading, \
                f"Navigation bug — expected '{expected_h1_title}', got '{heading}'"