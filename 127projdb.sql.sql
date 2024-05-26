--Create DB
DROP DATABASE IF EXISTS 127projdb;

CREATE OR REPLACE USER '127projdb'@'localhost' IDENTIFIED BY 'group5';
CREATE DATABASE 127projdb;
GRANT ALL ON 127projdb.* TO '127projdb'@'localhost';

USE 127projdb;

--user table
CREATE TABLE user (userid int(5) not null auto_increment, name varchar(50) default 'Anon', username varchar(15) not null, password varchar(20) not null, Primary Key(userid));
--user contact table
CREATE TABLE user_contact(userid int(5) not null, contactnum varchar(11) default 00000000000, Primary Key(userid, contactnum), CONSTRAINT user_contact_contactnum_fk FOREIGN KEY(`userid`) REFERENCES user(`userid`));
--Food establishments table (assumption: estabname not null)
CREATE TABLE food_estab(estabid int(5) not null auto_increment, estabname varchar(50) not null, branch_address varchar(50), rating decimal(3, 2) default 0, PRIMARY KEY(estabid));
--Food establishments contact table 
CREATE TABLE estab_contact(estabid int(5) not null, contactnum varchar(11)  default 00000000000, Primary Key(estabid, contactnum), CONSTRAINT estab_contact_contactnum_fk FOREIGN KEY(`estabid`) REFERENCES food_estab(`estabid`));
--Food Item table
CREATE TABLE food_item(productid int(5) not null auto_increment, itemname varchar(50) not null, price float(5) not null, rating decimal(3,2) default 0, estabid int(5) not null, PRIMARY KEY(productid), CONSTRAINT food_item_estabid_fk FOREIGN KEY(estabid) REFERENCES food_estab(estabid));
--Food type table
CREATE TABLE food_type(productid int(5) not null, foodtype varchar(20) not null, Primary Key(productid, foodtype),  CONSTRAINT food_type_foodtype_fk FOREIGN KEY(`productid`) REFERENCES food_item(`productid`));
--User reviews foodestab tables
CREATE TABLE user_reviews_foodestab(userid int(5) not null, estabid int(5) not null, rating decimal(3,2) default 0, date_of_review datetime, body varchar(200), Primary Key(userid, estabid, rating, date_of_review, body)); 
--USER Review item and establishment table
CREATE TABLE user_reviews_foodestab_item(userid int(5) not null, estabid int(5) not null, productid int(5) not null, rating decimal(3,2) default 0, date_of_review datetime, body varchar(200), Primary Key(userid, estabid, productid, rating, date_of_review, body)); 








--Insert dummy values
INSERT INTO user (userid, name,username, password) VALUES
        (1, 'Quejada', 'AkosiRoche123','AkosiRoche'),
        (2, 'Bañares', 'AkosiNaddine123','AkosiNaddine'),
        (3, 'Francisco','AkosiKen123','AkosiKen'),
        (4, 'Diares', 'AkosiClyde123','AkosiClyde'),
        (5, 'UP', 'UPNAMINGMAHAL12','UPNAMINGMAHAL');


INSERT INTO `user_contact` (`userid`,`contactnum`) VALUES
        (2, '12345678901'),
        (2,  '98765432101'),
        (4, '74185296301'),
        (4, '75395128461');


INSERT INTO `food_estab` (`estabid`, `estabname`, `branch_address`, `rating`) VALUES
        (1, 'Jollibee', 'Los Baños, Laguna', 5),
        (2, 'McDo', 'Sto. Tomas, Batangas', 4),
        (3, 'KFC','Taytay, Rizal',3),
        (4, 'BurgerKing', 'Dasmariñas, Cavite',2),
        (5, '711', 'Candelaria, Quezon',1);


INSERT INTO `estab_contact` (`estabid`,`contactnum`) VALUES
        (1, '14785296301'),
        (1,  '25896314701'),
        (3, '32165498701'),
        (3, '09090912345');




INSERT INTO `food_item` (`productid`,`itemname`, `price`, `rating`, `estabid`) VALUES
        (1, 'C1-Chicken Joy', 82.00, 5, 1),
        (2, 'Coke McFloat', 72.00, 4, 2),
        (3, 'A2-Combo',99.00, 5,3),
        (4, 'Whopper Jr', 75.00, 5, 4),
        (5, 'Big Byte', 100.00, 2, 5);


INSERT INTO `food_type` (`productid`,`foodtype`) VALUES
        (4, 'meat'),
        (4,  'vegetables'),
        (5, 'meat'),
        (5, 'chicken');




INSERT INTO `user_reviews_foodestab_item` (`userid`, `estabid`, `productid`, `rating`, `date_of_review`, `body`) VALUES 
       (1, 1, 1, 4, '2024-05-08', 'The food was delicious!'), 
       (2, 2, 2, 5, '2024-05-07', 'Excellent service and tasty meal.'),
       (3, 3, 3, 3, '2024-05-06', 'Average experience, nothing special.'),
       (4, 4, 4, 2, '2024-05-05', 'Disappointed with the quality of food.'),
       (5, 5, 5, 1, '2024-05-04', 'Would not recommend. Poor service.'),
       (1, 2, 3, 1, '2024-05-04', 'Would not recommend. Poor service.');


INSERT INTO `user_reviews_foodestab` (`userid`, `estabid`, `rating`, `date_of_review`, `body`)
VALUES 
(1, 1, 4, '2024-05-09', 'The food was delicious and the service was excellent.'),
(2, 1, 3, '2024-05-09', 'Food was okay, but service could be better.'),
(3, 2, 5, '2024-05-08', 'Best dining experience ever! Highly recommended.'),
(4, 3, 2, '2024-05-07', 'Disappointing food, wont be returning.');


