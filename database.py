from pymongo import MongoClient
from pymongo.database import Database
from datetime import datetime, UTC


def get_database(connection_string: str, mongo_db_name: str) -> Database:
    """Get MongoDB database instance."""
    
    try:
        client = MongoClient(connection_string)
        db = client[mongo_db_name]
        print("Database connection successful")
        return db
    except Exception as e:
        print("Connection failed:", e)
        raise


def yield_monitored_products(db: Database):
    """Yields monitored products from MongoDB."""
    
    monitored_collection = db["monitored"]
    
    pipeline = [
        {"$project": {
            "_id": 0,
            "url": 1,
            "variant_id": "$variant_id"
        }}
    ]
    
    try:
        cursor = monitored_collection.aggregate(pipeline)
        for product in cursor:
            yield product
    finally:
        cursor.close()


def yield_product_prices(db: Database):
    """Yields all retailers price history for each variant-region combination."""

    prices_collection = db["prices"]
    
    pipeline = [
        {"$sort": {"timestamp": -1}},

        {"$group": {
            "_id": {
                "variant_id": "$metadata.variant_id",
                "region_id": "$metadata.region_id"
            },
            "prices": {"$push": {
                "retailer_id": "$metadata.retailer_id",
                "price": "$price",
                "timestamp": "$timestamp"
            }}
        }},
        
        {"$project": {
            "_id": 0,
            "variant_id": "$_id.variant_id",
            "region_id": "$_id.region_id",
            "prices": 1
        }}
    ]
    
    try:
        cursor = prices_collection.aggregate(pipeline)
        for price in cursor:
            yield price
    finally:
        cursor.close()


def store_price(db: Database, product: dict, price: float) -> None:
    """Stores the given price in the database."""

    price_document = {
        "metadata": {
            "variant_id": product["variant_id"],
            "retailer_id": product["retailer_id"],
            "region_id": product["region_id"]
        },
        "timestamp": datetime.now(UTC),
        "price": price
    }

    prices_collection = db["prices"]
    prices_collection.insert_one(price_document)