import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform(datasets: dict) -> dict:
    """Limpia y transforma los DataFrames extraidos."""

    logger.info("Iniciando transformacion de datos...")

    # -- customers --
    customers = datasets["customers"].copy()
    customers.drop_duplicates(subset="customer_id", inplace=True)
    customers.dropna(subset=["customer_id", "customer_unique_id"], inplace=True)
    customers.columns = [
        "customer_id", "customer_unique_id",
        "customer_zip_code", "customer_city", "customer_state"
    ]
    logger.info(f"  customers: {len(customers):,} registros limpios")

    # -- sellers --
    sellers = datasets["sellers"].copy()
    sellers.drop_duplicates(subset="seller_id", inplace=True)
    sellers.dropna(subset=["seller_id"], inplace=True)
    sellers.columns = [
        "seller_id", "seller_zip_code",
        "seller_city", "seller_state"
    ]
    logger.info(f"  sellers: {len(sellers):,} registros limpios")

    # -- categories --
    categories = datasets["categories"].copy()
    categories.drop_duplicates(inplace=True)
    categories.columns = ["category_name", "category_name_english"]
    logger.info(f"  categories: {len(categories):,} registros limpios")

    # -- products --
    products = datasets["products"].copy()
    products.drop_duplicates(subset="product_id", inplace=True)
    products.dropna(subset=["product_id"], inplace=True)
    products.columns = [
        "product_id", "category_name", "product_name_length",
        "product_desc_length", "product_photos_qty",
        "product_weight_g", "product_length_cm",
        "product_height_cm", "product_width_cm"
    ]
    logger.info(f"  products: {len(products):,} registros limpios")

    # -- orders --
    orders = datasets["orders"].copy()
    orders.drop_duplicates(subset="order_id", inplace=True)
    orders.dropna(subset=["order_id", "customer_id"], inplace=True)

    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    orders.columns = [
        "order_id", "customer_id", "order_status",
        "order_purchase_ts", "order_approved_ts",
        "order_delivered_carrier", "order_delivered_customer",
        "order_estimated_delivery"
    ]
    logger.info(f"  orders: {len(orders):,} registros limpios")

    # -- order_items --
    order_items = datasets["order_items"].copy()
    order_items.drop_duplicates(inplace=True)
    order_items.dropna(subset=["order_id", "product_id", "seller_id"], inplace=True)
    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"], errors="coerce"
    )
    logger.info(f"  order_items: {len(order_items):,} registros limpios")

    # -- payments --
    payments = datasets["payments"].copy()
    payments.drop_duplicates(inplace=True)
    payments.dropna(subset=["order_id"], inplace=True)
    logger.info(f"  payments: {len(payments):,} registros limpios")

    # -- reviews --
    reviews = datasets["reviews"].copy()
    reviews.drop_duplicates(subset="review_id", inplace=True)
    reviews.dropna(subset=["review_id", "order_id"], inplace=True)
    reviews["review_creation_date"] = pd.to_datetime(
        reviews["review_creation_date"], errors="coerce"
    )
    reviews["review_answer_timestamp"] = pd.to_datetime(
        reviews["review_answer_timestamp"], errors="coerce"
    )
    reviews = reviews[[
        "review_id", "order_id", "review_score",
        "review_comment_message",
        "review_creation_date", "review_answer_timestamp"
    ]]
    reviews.columns = [
        "review_id", "order_id", "review_score",
        "review_comment", "review_created", "review_answered"
    ]
    logger.info(f"  reviews: {len(reviews):,} registros limpios")

    logger.info("Transformacion completada.")

    return {
        "customers":   customers,
        "sellers":     sellers,
        "product_categories": categories,
        "products":    products,
        "orders":      orders,
        "order_items": order_items,
        "order_payments": payments,
        "order_reviews":  reviews,
    }
