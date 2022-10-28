CREATE OR REPLACE FUNCTION popular_products()
RETURNS TABLE (
    product int
) AS $$
BEGIN
    DROP TABLE IF EXISTS popular_products;

    CREATE TEMP TABLE popular_products(
        product int
    );

    INSERT INTO popular_products (product)
    WITH tmp AS (
	SELECT product_id, COUNT(app_orders_products.id) AS count_products
	FROM app_orders_products
	GROUP BY product_id
	ORDER BY count_products DESC)
    SELECT product_id FROM tmp;

    RETURN QUERY SELECT * FROM popular_products;
END;
$$ language PLPGSQL;

CREATE OR REPLACE FUNCTION total_price(integer)
RETURNS INT AS $$
BEGIN
    RETURN (WITH TMP(product_id, cost, cnt, total) AS 
        (SELECT product_id, cost, cnt, cost*cnt AS total
		FROM app_order JOIN app_orders_products 
        ON app_order.id=app_orders_products.order_id
        JOIN app_product ON app_product.id=app_orders_products.product_id 
        WHERE app_order.id=$1)
    SELECT SUM(total) AS total_price FROM TMP);
END;
$$ language PLPGSQL;