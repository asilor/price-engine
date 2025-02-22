from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from os import getenv
from database import get_database, yield_monitored_products, yield_product_prices
from proxies import ProxyRotator, get_proxies
from prestashop import get_access_token
from check_prices import check_price
from process_prices import process_price


def main() -> None:
    load_dotenv()

    mongo_ip = getenv("MONGO_IP")
    mongo_port = int(getenv("MONGO_PORT"))
    mongo_user = getenv("MONGO_USER")
    mongo_password = getenv("MONGO_PASSWORD")
    mongo_db_name = getenv("MONGO_DB_NAME")

    connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_ip}:{mongo_port}"

    db = get_database(connection_string, mongo_db_name)
    proxies = get_proxies()
    proxy_rotator = ProxyRotator(proxies)

    num_workers_check = int(getenv("NUM_WORKERS_CHECK"))

    with ThreadPoolExecutor(max_workers=num_workers_check) as executor:
        for product in yield_monitored_products(db):
            executor.submit(check_price, db, proxy_rotator, product)

    base_url = getenv("PRESTASHOP_BASE_URL")
    client_id = getenv("PRESTASHOP_CLIENT_ID")
    client_secret = getenv("PRESTASHOP_CLIENT_SECRET")

    access_token = get_access_token(base_url, client_id, client_secret)

    num_workers_process = int(getenv("NUM_WORKERS_PROCESS"))

    with ThreadPoolExecutor(max_workers=num_workers_process) as executor:
        for prices in yield_product_prices(db):
            executor.submit(process_price, db, prices, base_url, access_token)


if __name__ == "__main__":
    main()