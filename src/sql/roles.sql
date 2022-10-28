CREATE ROLE Client NOSUPERUSER NOCREATEDB;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO Client;
GRANT INSERT, UPDATE ON auth_user TO Client;
GRANT INSERT, UPDATE ON app_profile TO Client;
GRANT INSERT ON app_review TO Client;
GRANT INSERT, UPDATE ON app_likeproduct TO Client;
GRANT INSERT, UPDATE ON app_likereview TO Client;

CREATE ROLE Manager NOSUPERUSER NOCREATEDB;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO Manager;
GRANT ALL PRIVILEGES ON app_order TO Manager;
GRANT ALL PRIVILEGES ON app_product TO Manager;
GRANT ALL PRIVILEGES ON app_category TO Manager;
GRANT ALL PRIVILEGES ON app_review TO Manager;
GRANT ALL PRIVILEGES ON app_product_categories TO Manager;
GRANT ALL PRIVILEGES ON app_orders_products TO Manager;

CREATE ROLE Administrator CREATEROLE NOSUPERUSER NOCREATEDB;
GRANT ALL PRIVILEGES ON auth_user TO Administrator;
GRANT ALL PRIVILEGES ON app_profile TO Administrator;
GRANT ALL PRIVILEGES ON app_product TO Administrator;
GRANT ALL PRIVILEGES ON app_order TO Administrator;
GRANT ALL PRIVILEGES ON app_category TO Administrator;
GRANT ALL PRIVILEGES ON app_review TO Administrator;
GRANT ALL PRIVILEGES ON app_likeproduct TO Administrator;
GRANT ALL PRIVILEGES ON app_likereview TO Administrator;
GRANT ALL PRIVILEGES ON app_product_categories TO Administrator;
GRANT ALL PRIVILEGES ON app_orders_products TO Administrator;