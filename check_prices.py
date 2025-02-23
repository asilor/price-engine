
from database import Database
from proxies import ProxyRotator
from retailers.amazon import check_amazon_price
from retailers.tradeinn import check_tradeinn_price
from retailers.pccomponentes import check_pccomponentes_price
from retailers.bigbuy import check_bigbuy_price
from retailers.allzone import check_allzone_price


def check_price(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    """Check the price of the given product and store it in the database."""

    url = str(product["url"])
    
    if "amazon" in url: check_amazon_price(db, proxy_rotator, product)
    elif "tradeinn" in url: check_tradeinn_price(db, proxy_rotator, product)
    elif "pccomponentes" in url: check_pccomponentes_price(db, proxy_rotator, product)
    elif "bigbuy" in url: check_bigbuy_price(db, proxy_rotator, product)
    elif "allzone" in url: check_allzone_price(db, proxy_rotator, product)
    else: print(f"Unknown retailer: {url}")
