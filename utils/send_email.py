import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into os.environ

from_email = os.getenv("EMAIL_FROM")
password   = os.getenv("EMAIL_PASSWORD")
to_email   = os.getenv("EMAIL_TO", "").split(",")  # supports multiple: "a@x.com,b@x.com"

