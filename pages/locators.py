



class HomePageLocators:
    LOGIN_ICON = 'xpath=//*[@id="site-header-inner"]/div[3]/div/a[1]/i'
    LOGO_IMAGE = 'css=img.site-logo'
    WISHLIST = '//*[@id="site-header-inner"]/div[3]/div/a[2]/i'
    CART = '//*[@id="site-header-inner"]/div[3]/div/div/a/span/span/span'
    TEA_MENU = '//*[@id="menu-item-1766"]/a/span'
    TEAWARE_MENU = '//*[@id="menu-item-11530"]/a/span/span/text()'

class LoginPageLocators:
    USERNAME_FIELD = 'xpath=//*[@id="username"]'
    PASSWORD_FIELD = 'id=password'
    LOGIN_BUTTON = '[name="login"]'
    ERROR_MESSAGE = 'xpath=//*[@id="error_message"]'