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
        #Click each header category and verify it lands on the right page.
        home_page = setup_all_page["home"]
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



    def test_submenu_item_hover_color_changes(self,setup_all_page):
        home_page = setup_all_page["home"]
        home_page.hover_tea_types_menu()
        home_page.page.wait_for_load_state("domcontentloaded")

        menu_items = ["Choose tea", "Flavors", "Feelings", "Activities", "Time for Tea", "Tea & Health"]

        for item in menu_items:
            #print(f"\n--- Testing: {item}---")

            #is_highlighted = home_page.is_submenu_item_highlighted(item)
            #bg_color = home_page.get_submenu_item_bg_color(item)

            #print(f"Item: {item}")
            #print(f"Highlighted: {is_highlighted}")
            #print(f"Background color: {bg_color}")

            #assert is_highlighted, f"Item '{item}' NOT highlighted. Color: {bg_color}"

            assert home_page.is_submenu_item_highlighted(item), \
                f"'{item}' should highlight on hover"

        print(f"All {len(menu_items)} menu items highlight correctly")

