



class HomePageLocators:
    #icons
    LOGIN_ICON = 'xpath=//*[@id="site-header-inner"]/div[3]/div/a[1]/i'
    LOGO_IMAGE = '//*[@id="site-logo-inner"]/a[1]/img'
    WISHLIST_PATH = '//*[@id="site-header-inner"]/div[3]/div/a[2]/i'
    CART = '//*[@id="site-header-inner"]/div[3]/div/div/a/span/span/span'
    LANGUAGE = '//*[@id="site-header-inner"]/div[3]/div/ul/li/ul/li[1]'
    CART_ICON = 'a.wcmenucart-shortcode:visible'
    # CSS Locators
    WISHLIST_VISIBLE = '#site-header-inner a[href*="wishlist"]:visible'
    CART_ICON_VISIBLE = '#site-header-inner a.wcmenucart-shortcode:visible'
    #menu
    TEA_MENU = '#site-header-inner a[href="https://itea.co.il/en/tea/"]'
    TEAWARE_MENU = '#menu-item-11530 > a'
    COFFEE_MENU = '#site-header-inner a[href="https://itea.co.il/en/coffee/"]'
    #drodown
    TEATYPES = '//*[@id="menu-item-6524"]'
    MATCHA_MENU = '//*[@id="menu-item-11584"]/a'
    SALE_MENU = '//*[@id="menu-item-6565"]/a'

class LoginPageLocators:
    USERNAME_FIELD = 'xpath=//*[@id="username"]'
    PASSWORD_FIELD = 'id=password'
    LOGIN_BUTTON = '[name="login"]'
    ERROR_MESSAGE = 'xpath=//*[@id="error_message"]'

class TeaPageLocators:
    # unordered list off all tea
    PRODUCT_LIST = '//*[@id="content"]/article/ul'
    PRODUCT_ITEM = 'li.product'
    PRODUCT_TITLE = 'li.title.desktop a'
    PRODUCT_PRICE = 'li.product .price'
    ADD_TO_CART_BTN = 'a.add_to_cart_button'
    ADD_TO_WISHLIST_BTN = 'button.yith-wcwl-add-to-wishlist-button'
    SINGLE_PRODUCT_WISHLIST_BTN = '.summary .yith-wcwl-add-to-wishlist-button'
    SORTING_DROPDOWN = 'select.orderby'
    PAGE_TITLE_H1 = 'h1.page-header-title'
    SIMPLE_PRODUCT_ITEM = 'li.product:has(a.product_type_simple)'
    SELECT_OPTIONS_PRODUCT_ITEM = 'li.product:has(a.product_type_variable, a.product_type_bundle)'

class TeawarePageLocators:
    PAGE_TITLE = 'h1.page-header-title'

class CartPageLocators:
    QUANTITY_INPUT = 'input.qty'
    UPDATE_CART_BTN = 'button[name="update_cart"]'
    MINUS_BTN = 'a.minus'
    PLUS_BTN = 'a.plus'
    REMOVE_ITEM = 'a.remove'
    CART_ITEM = 'tr.wc_cart_item'
    EMPTY_CART_MSG = 'p.cart-empty'
    CART_TOTALS = 'h2.widget_shopping_cart_total'