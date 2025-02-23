from database import Database, store_price
from bson.objectid import ObjectId
from proxies import ProxyRotator
from selectolax.parser import HTMLParser


BIGBUY_ID = "67bb99b721cc010007e2795d"


def check_bigbuy_price(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    """Checks the price of the given product and stores it in the database."""

    url = str(product["url"])
    html = proxy_rotator.get_content(url)

    price = parse_bigbuy_price(html)
    region_id = "67942b3721cc010007e278df" # España
 
    product["region_id"] = ObjectId(region_id)
    product["retailer_id"] = ObjectId(BIGBUY_ID)

    store_price(db, product, price)
    print(f"url: {url}, region_id: {region_id}, price: {price}")


def parse_bigbuy_price(html: str) -> float:
    """Given the bigbuy product page HTML, return the price."""

    tree = HTMLParser(html)

    price_element = tree.css_first('span[itemprop="price"]')

    if not price_element:
        return 0.0

    price_text = price_element.text().strip()
    price_text = price_text.replace('€', '').replace('.', '').replace(',', '.').strip()

    return float(price_text)
