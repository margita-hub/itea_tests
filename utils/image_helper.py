import hashlib
import os

import requests

from pages.home_page import REFERENCE_DIR, REFERENCE_HASH


class ImageHashHelper:
    def compute_image_md5(self, url: str) -> str:
        src = self.get_logo_src()
        response = requests.get(src, timeout=10, verify=False)  # verify=False skips SSL check
        response.raise_for_status()
        return hashlib.md5(response.content).hexdigest()

    def save_reference_hash(self, hash_value: str):
        os.makedirs(REFERENCE_DIR, exist_ok=True)
        with open(REFERENCE_HASH, "w") as f:
            f.write(hash_value)

    def get_logo_src(self) -> str:
        return self.get_logo_img().get_attribute("src")

    def load_reference_hash(self) -> str:
        with open(REFERENCE_HASH, "r") as f:
            return f.read().strip()

    def reference_hash_exists(self) -> bool:
        return os.path.exists(REFERENCE_HASH)
