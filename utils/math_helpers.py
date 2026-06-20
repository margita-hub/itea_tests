import math

def calculate_qty_for_free_shipping(item_price: float, threshold: float = 200.0) -> int:
    #How many of this item are needed to reach the free shipping threshold?
    if item_price <= 0:
        raise ValueError(f"Item price must be > 0, got {item_price}")
    return math.ceil(threshold / item_price) + 1