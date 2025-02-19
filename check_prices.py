
from database import Database
from proxies import ProxyRotator
from retailers.amazon import get_amazon_price
from retailers.tradeinn import get_tradeinn_prices
from retailers.pccomponentes import get_pccomponentes_prices


def check_price(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    """Check the price of the given product and store it in the database."""

    url = str(product["url"])
    
    if "amazon" in url: get_amazon_price(db, proxy_rotator, product)
    elif "tradeinn" in url: get_tradeinn_prices(db, proxy_rotator, product)
    elif "pccomponentes" in url: get_pccomponentes_prices(db, proxy_rotator, product)
    else: print(f"Unknown retailer: {url}")
