import json
import os


def load_products_from_db():
    #Reads expected products from the test_data/db.json file.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Get the absolute path to the db.json file
    file_path = os.path.join(base_dir, "test_data", "db.json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["products"]