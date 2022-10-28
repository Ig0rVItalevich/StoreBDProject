CREATE OR REPLACE FUNCTION decrease_count()
RETURNS TRIGGER
AS $decrease_count$
BEGIN
    UPDATE app_product 
    SET count = count - NEW.cnt
    WHERE app_product.id = NEW.product_id;
    RETURN NEW;
END;
$decrease_count$ language PLPGSQL;

CREATE TRIGGER decrease_count AFTER INSERT ON app_orders_products
FOR EACH ROW EXECUTE PROCEDURE decrease_count();


CREATE OR REPLACE FUNCTION increase_count()
RETURNS TRIGGER
AS $increase_count$
BEGIN
    UPDATE app_product 
    SET count = count + OLD.cnt
    WHERE app_product.id = OLD.product_id;
    RETURN OLD;
END;
$increase_count$ language PLPGSQL;

CREATE TRIGGER increase_count AFTER DELETE ON app_orders_products
FOR EACH ROW EXECUTE PROCEDURE increase_count();


CREATE OR REPLACE FUNCTION like_product_insert()
RETURNS TRIGGER
AS $like_product_insert$
BEGIN
    UPDATE app_product 
    SET rating = rating + NEW.mark
    WHERE app_product.id = NEW.product_id;
    RETURN NEW;
END;
$like_product_insert$ language PLPGSQL;

CREATE TRIGGER like_product_insert AFTER INSERT ON app_likeproduct
FOR EACH ROW EXECUTE PROCEDURE like_product_insert();


CREATE OR REPLACE FUNCTION like_product_update()
RETURNS TRIGGER
AS $like_product_update$
BEGIN
    UPDATE app_product
    SET rating = rating + 2 * NEW.mark
    WHERE app_product.id = NEW.product_id;
    RETURN NEW;
END;
$like_product_update$ language PLPGSQL;

CREATE TRIGGER like_product_update AFTER UPDATE ON app_likeproduct
FOR EACH ROW EXECUTE PROCEDURE like_product_update();


CREATE OR REPLACE FUNCTION like_review_insert()
RETURNS TRIGGER
AS $like_review_insert$
BEGIN
    UPDATE app_review
    SET rating = rating + NEW.mark
    WHERE app_review.id = NEW.review_id;
    RETURN NEW;
END;
$like_review_insert$ language PLPGSQL;

CREATE TRIGGER like_review_insert AFTER INSERT ON app_likereview
FOR EACH ROW EXECUTE PROCEDURE like_review_insert();


CREATE OR REPLACE FUNCTION like_review_update()
RETURNS TRIGGER
AS $like_review_update$
BEGIN
    UPDATE app_review
    SET rating = rating + 2 * NEW.mark
    WHERE app_review.id = NEW.review_id;
    RETURN NEW;
END;
$like_review_update$ language PLPGSQL;

CREATE TRIGGER like_review_update AFTER UPDATE ON app_likereview
FOR EACH ROW EXECUTE PROCEDURE like_review_update();

CREATE OR REPLACE FUNCTION create_review()
RETURNS TRIGGER
AS $create_review$
BEGIN
    IF NEW.product_id IN (
        SELECT product_id FROM app_orders_products JOIN app_order
        ON app_orders_products.order_id = app_order.id
        WHERE app_order.profile_id = NEW.profile_id
    ) THEN
        INSERT INTO app_review (content, review_date, rating, product_id, profile_id)
        VALUES (NEW.content, NEW.review_date, NEW.rating, NEW.product_id, NEW.profile_id);
        RETURN NEW;
END;
$create_review$ language PLPGSQL;

CREATE TRIGGER create_review INSTEAD OF INSERT ON app_review
FOR EACH ROW EXECUTE PROCEDURE create_review();