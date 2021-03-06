--- "TRANSACTION" TABLE CREATION
CREATE TABLE TRANSACTION (
    date date,
    order_id int,
    client_id int,
    prod_id int,
    prod_price float,
    prod_qty int
);

--- VALUES INSERTION INTO "TRANSACTION"
INSERT INTO TRANSACTION VALUES ('01/01/20', 1234, 999, 490756, 50, 1);
INSERT INTO TRANSACTION VALUES ('01/01/20', 1234, 999, 389728, 3.56, 4);
INSERT INTO TRANSACTION VALUES ('01/01/20', 3456, 845, 490756, 50, 2);
INSERT INTO TRANSACTION VALUES ('01/01/20', 3456, 845, 549380, 300, 1);
INSERT INTO TRANSACTION VALUES ('01/01/20', 3456, 845, 293718, 10, 6);

--- "PRODUCT_NOMENCLATURE" TABLE CREATION
CREATE TABLE PRODUCT_NOMENCLATURE (
    product_id int,
    product_type varchar,
    product_name varchar
);

--- VALUES INSERTION INTO "PRODUCT_NOMENCLATURE"
INSERT INTO PRODUCT_NOMENCLATURE VALUES (490756, 'MEUBLE', 'Chaise');
INSERT INTO PRODUCT_NOMENCLATURE VALUES (389728, 'DECO', 'Boule de Noël');
INSERT INTO PRODUCT_NOMENCLATURE VALUES (549380, 'MEUBLE', 'Canapé');
INSERT INTO PRODUCT_NOMENCLATURE VALUES (293718, 'DECO', 'Mug');