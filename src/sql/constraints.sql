ALTER TABLE app_product
    ADD CONSTRAINT correct_count CHECK (count>=0);

ALTER TABLE app_product
    ADD CONSTRAINT correct_volume CHECK (volume>0 AND volume<=200);

ALTER TABLE app_product
    ADD CONSTRAINT correct_cost CHECK (cost>=0);

ALTER TABLE app_orders_products
    ADD CONSTRAINT correct_cnt CHECK (cnt>=0);

ALTER TABLE app_likeproduct
    ADD CONSTRAINT correct_mark_likeproduct CHECK (mark>=-1 AND mark<=1);

ALTER TABLE app_likereview
    ADD CONSTRAINT correct_mark_likereview CHECK (mark>=-1 AND mark<=1);

ALTER TABLE app_profile
    ADD CONSTRAINT correct_sex CHECK (sex = 'Male' OR sex = 'Female');