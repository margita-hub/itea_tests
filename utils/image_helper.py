import hashlib
import os
import requests


class ImageHashHelper:
    def compute_image_md5(self, url: str) -> str:
        response = requests.get(url, timeout=10, verify=False)  # ← uses url directly
        response.raise_for_status()
        return hashlib.md5(response.content).hexdigest()

    def save_reference_hash(self, hash_value: str):
        os.makedirs("reference_images", exist_ok=True)
        with open("reference_images/logo_hash.txt", "w") as f:
            f.write(hash_value)



    def load_reference_hash(self) -> str:
        with open("reference_images/logo_hash.txt", "r") as f:
            return f.read().strip()

    def reference_hash_exists(self) -> bool:
        return os.path.exists("reference_images/logo_hash.txt")
