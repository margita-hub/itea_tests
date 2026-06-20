import os
from dotenv import load_dotenv
load_dotenv()

URL_HE       = "https://itea.co.il/"
URL_EN       = "https://itea.co.il/en/"
URL_RU       = "https://itea.co.il/ru/"
TEA_URL      = "https://itea.co.il/en/tea/"
TEAWARE_URL  = "https://itea.co.il/en/teaware/"
CART_URL     = "https://itea.co.il/en/cart/"
WISHLIST_URL = "https://itea.co.il/en/wishlist/"
LOGIN_URL    = "https://itea.co.il/en/my-account/"
ORDERS_URL   = "https://itea.co.il/en/my-account/orders/"
SALE_URL     = "https://itea.co.il/en/sale/"
COFFEE_URL   = "https://itea.co.il/en/coffee/"
MATCHA_URL   = "https://itea.co.il/en/matcha/"

VALID_CREDENTIALS = {
    "email":    os.getenv("ITEA_EMAIL"),
    "password": os.getenv("ITEA_PASSWORD"),
}




