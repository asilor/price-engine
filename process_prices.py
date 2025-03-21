from database import Database, store_price
from bson.objectid import ObjectId
from prestashop import update_product_price


ASILOR_ID = "67b2232121cc010007e27943"


def process_price(db: Database, prices: dict, base_url: str, access_token: str):
    """Compute optimal price, store it in the database and update it on the website."""

    optimal_price = compute_optimal_price(prices)

    product = {
        "variant_id": ObjectId(prices["variant_id"]),
        "retailer_id": ObjectId(ASILOR_ID),
        "region_id": ObjectId(prices["region_id"]) 
    }

    store_price(db, product, optimal_price)

    product_id = prices["prestashop_id"]

    TAX_RATE = 21
    optimal_price_no_tax = round(optimal_price * 100 / (100 + TAX_RATE), 2)
    
    update_product_price(base_url, access_token, product_id, optimal_price_no_tax)


def compute_optimal_price(prices: dict) -> float:
    """Compute optimal price by finding lowest price among most recent retailer prices."""

    latest_prices = {}
    for price in prices['prices']:
        retailer_id = str(price['retailer_id'])
        if retailer_id not in latest_prices and retailer_id != ASILOR_ID:
            latest_prices[retailer_id] = price['price']

    ajust = -2
    optimal_price = min(price for price in latest_prices.values() if price > 0) + ajust

    return optimal_price
