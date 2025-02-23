from database import Database, store_price
from bson.objectid import ObjectId
from proxies import ProxyRotator
from selectolax.parser import HTMLParser


ALLZONE_ID = "67bb9ff621cc010007e27961"


def check_allzone_price(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    """Checks the price of the given product and stores it in the database."""

    url = str(product["url"])
    html = proxy_rotator.get_content(url)

    price = parse_allzone_price(html)
    region_id = "67942b3721cc010007e278df" # España
 
    product["region_id"] = ObjectId(region_id)
    product["retailer_id"] = ObjectId(ALLZONE_ID)

    store_price(db, product, price)
    print(f"url: {url}, region_id: {region_id}, price: {price}")


def parse_allzone_price(html: str) -> float:
    """Given the allzone product page HTML, return the price."""

    tree = HTMLParser(html)

    price_element = tree.css_first('span[itemprop="price"][content]')

    if not price_element:
        return 0.0

    return float(price_element.attributes['content'])
