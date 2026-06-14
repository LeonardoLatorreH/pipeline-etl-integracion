-- Esquema de base de datos destino
-- Pipeline ETL — Brazilian E-Commerce Olist
--  MySQL

CREATE DATABASE IF NOT EXISTS olist_etl;
USE olist_etl;

-- Clientes
CREATE TABLE IF NOT EXISTS customers (
    customer_id          VARCHAR(50)  NOT NULL,
    customer_unique_id   VARCHAR(50)  NOT NULL,
    customer_zip_code    VARCHAR(10),
    customer_city        VARCHAR(100),
    customer_state       VARCHAR(5),
    CONSTRAINT PK_customers PRIMARY KEY (customer_id)
);

-- Vendedores
CREATE TABLE IF NOT EXISTS sellers (
    seller_id         VARCHAR(50)  NOT NULL,
    seller_zip_code   VARCHAR(10),
    seller_city       VARCHAR(100),
    seller_state      VARCHAR(5),
    CONSTRAINT PK_sellers PRIMARY KEY (seller_id)
);

-- Categorías de productos
CREATE TABLE IF NOT EXISTS product_categories (
    category_name            VARCHAR(100) NOT NULL,
    category_name_english    VARCHAR(100),
    CONSTRAINT PK_categories PRIMARY KEY (category_name)
);

-- Productos
CREATE TABLE IF NOT EXISTS products (
    product_id           VARCHAR(50)  NOT NULL,
    category_name        VARCHAR(100),
    product_name_length  INT,
    product_desc_length  INT,
    product_photos_qty   INT,
    product_weight_g     INT,
    product_length_cm    INT,
    product_height_cm    INT,
    product_width_cm     INT,
    CONSTRAINT PK_products PRIMARY KEY (product_id)
);

-- Órdenes
CREATE TABLE IF NOT EXISTS orders (
    order_id                VARCHAR(50)  NOT NULL,
    customer_id             VARCHAR(50)  NOT NULL,
    order_status            VARCHAR(20),
    order_purchase_ts       DATETIME,
    order_approved_ts       DATETIME,
    order_delivered_carrier DATETIME,
    order_delivered_customer DATETIME,
    order_estimated_delivery DATETIME,
    CONSTRAINT PK_orders PRIMARY KEY (order_id),
    CONSTRAINT FK_orders_customers FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Items de órdenes
CREATE TABLE IF NOT EXISTS order_items (
    order_id             VARCHAR(50)  NOT NULL,
    order_item_id        INT          NOT NULL,
    product_id           VARCHAR(50)  NOT NULL,
    seller_id            VARCHAR(50)  NOT NULL,
    shipping_limit_date  DATETIME,
    price                DECIMAL(10,2),
    freight_value        DECIMAL(10,2),
    CONSTRAINT PK_order_items PRIMARY KEY (order_id, order_item_id),
    CONSTRAINT FK_items_orders   FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    CONSTRAINT FK_items_products FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT FK_items_sellers  FOREIGN KEY (seller_id)  REFERENCES sellers(seller_id)
);

-- Pagos
CREATE TABLE IF NOT EXISTS order_payments (
    order_id              VARCHAR(50) NOT NULL,
    payment_sequential    INT         NOT NULL,
    payment_type          VARCHAR(20),
    payment_installments  INT,
    payment_value         DECIMAL(10,2),
    CONSTRAINT PK_payments PRIMARY KEY (order_id, payment_sequential),
    CONSTRAINT FK_payments_orders FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Reviews
CREATE TABLE IF NOT EXISTS order_reviews (
    review_id         VARCHAR(50) NOT NULL,
    order_id          VARCHAR(50) NOT NULL,
    review_score      INT,
    review_comment    TEXT,
    review_created    DATETIME,
    review_answered   DATETIME,
    CONSTRAINT PK_reviews PRIMARY KEY (review_id),
    CONSTRAINT FK_reviews_orders FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
