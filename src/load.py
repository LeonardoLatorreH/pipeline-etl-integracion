import logging
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

def load(datasets: dict, connection_string: str) -> None:
    """Carga los DataFrames transformados a MySQL."""

    logger.info("Iniciando carga de datos a MySQL...")

    engine = create_engine(connection_string)

    # orden de carga respeta las foreign keys
    load_order = [
        "customers",
        "sellers",
        "product_categories",
        "products",
        "orders",
        "order_items",
        "order_payments",
        "order_reviews",
    ]

    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

    for table in load_order:
        df = datasets[table]
        try:
            df.to_sql(
                name=table,
                con=engine,
                if_exists="replace",
                index=False,
                chunksize=1000,
            )
            logger.info(f"  {table}: {len(df):,} registros cargados")
        except Exception as e:
            logger.error(f"  Error cargando {table}: {e}")
            raise

    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    logger.info("Carga completada.")
