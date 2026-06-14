import logging
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

def load(datasets: dict, connection_string: str) -> None:

    logger.info("Iniciando carga de datos a MySQL...")

    engine = create_engine(connection_string)

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

    # Validación básica de datasets
    missing_tables = [t for t in load_order if t not in datasets]
    if missing_tables:
        logger.warning(f"Tablas faltantes en datasets: {missing_tables}")

    with engine.begin() as conn:

        # Desactivar foreign keys temporalmente
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        for table in load_order:

            if table not in datasets:
                logger.warning(f"Saltando {table}: no existe en datasets")
                continue

            df = datasets[table]

            if df is None or df.empty:
                logger.warning(f"Saltando {table}: DataFrame vacío")
                continue

            try:
                logger.info(f"Iniciando carga de {table}")

                # Limpieza básica de duplicados
                df = df.drop_duplicates()

                df.to_sql(
                    name=table,
                    con=conn,
                    if_exists="append",
                    index=False,
                    chunksize=1000,
                    method="multi"
                )

                logger.info(f"{table}: {len(df):,} registros cargados")

            except Exception as e:
                logger.error(f"Error cargando {table}: {e}")
                raise

        # Reactivar foreign keys
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    logger.info("Carga completada exitosamente.")
