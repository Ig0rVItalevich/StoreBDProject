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
        (SELECT product_id, app_orders_products.cost, cnt, app_orders_products.cost*cnt AS total
		FROM app_order JOIN app_orders_products 
        ON app_order.id=app_orders_products.order_id
        JOIN app_product ON app_product.id=app_orders_products.product_id 
        WHERE app_order.id=$1)
    SELECT SUM(total) AS total_price FROM TMP);
END;
$$ language PLPGSQL;

CREATE OR REPLACE FUNCTION staff_actions()
RETURNS TABLE (
    entity varchar(100),
    entity_id text,
    user_id integer,
    action_description text,
    action_time timestamp with time zone
) AS $$
BEGIN
    DROP TABLE IF EXISTS staff_actions;

    CREATE TEMP TABLE staff_actions(
        entity varchar(100),
        entity_id text,
        usr_id integer,
        action_description text,
        act_time timestamp with time zone
    );

    INSERT INTO staff_actions(entity, entity_id, usr_id, action_description, act_time)
    WITH tmp AS (
	SELECT model, 
		object_id, 
		django_admin_log.user_id as usr_id, 
		change_message, 
		django_admin_log.action_time as act_time
    FROM django_admin_log 
    JOIN django_content_type ON django_admin_log.content_type_id = django_content_type.id
    WHERE DATE(django_admin_log.action_time) = CURRENT_DATE)
    SELECT model, object_id, usr_id, change_message, act_time FROM tmp;

    RETURN QUERY SELECT * FROM staff_actions;
END;
$$ language PLPGSQL;