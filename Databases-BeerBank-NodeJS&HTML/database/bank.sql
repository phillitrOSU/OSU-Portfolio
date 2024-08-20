SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;


CREATE OR REPLACE TABLE Styles (
style_ID int NOT NULL AUTO_INCREMENT,
style_Name varchar(45) NOT NULL,
PRIMARY KEY (style_ID)
);

CREATE OR REPLACE TABLE Breweries (
brewery_ID int NOT NULL AUTO_INCREMENT,
specialty int NOT NULL,
brewery_Name varchar(45) NOT NULL,
region varchar(45),
PRIMARY KEY (brewery_ID),
FOREIGN KEY (specialty) REFERENCES Styles(style_ID)
);


CREATE OR REPLACE TABLE Beer (
beer_ID int NOT NULL AUTO_INCREMENT,
style int NOT NULL,
brewery int NOT NULL,
inventory int NOT NULL,
beer_Name varchar(45) NOT NULL,
price decimal(6,2),
year year(4),
PRIMARY KEY (beer_ID),
FOREIGN KEY (style) REFERENCES Styles(style_ID),
FOREIGN KEY (brewery) REFERENCES Breweries(brewery_ID)
);

CREATE OR REPLACE TABLE Customers (
customer_ID int NOT NULL AUTO_INCREMENT,
customer_Name varchar(45),
address varchar(45),
phone varchar(45),
PRIMARY KEY (customer_ID)
);

CREATE OR REPLACE TABLE Orders (
orders_ID int NOT NULL AUTO_INCREMENT,
customer int NOT NULL,
total_Sales decimal(6,2) NOT NULL,
total_Beers int NOT NULL,
date datetime NOT NULL,
PRIMARY KEY (orders_ID),
FOREIGN KEY (customer) REFERENCES Customers(customer_ID)
);

CREATE OR REPLACE TABLE Beer_Orders (
sales_ID int NOT NULL AUTO_INCREMENT,
product_ID int not NULL,
invoice_ID int not NULL,
quantity int,
total_Price decimal(6,2) NOT NULL,
PRIMARY KEY (sales_ID),
FOREIGN KEY (product_ID) REFERENCES Beer(beer_ID),
FOREIGN KEY (invoice_ID) REFERENCES Orders(orders_ID)
);


INSERT INTO Customers (customer_name, address, phone)
VALUES ('Joe Deckerd', '1243 Hill Blvd, San Jose, CA 87412', '344-430-1234'),
('Chris Tally', '140 Ridge Ln, Austin, TX 12034', '512-230-4032'),
('Benjamin Hooper', '129 Stateside, Shreveport, LA 39021', '412-239-1230');

INSERT INTO Styles (style_Name)
VALUES ('Imperial Pale Ale (IPA)'),
('Milk Stout'),
('Hefeweizen'),
('Pilsner'),
('Lager'),
('Brown Ale');

INSERT INTO Breweries (specialty, brewery_Name, region)
VALUES (1, 'IPA Central', 'West Coast'),
(2, 'Desert Sun', 'Southwest'),
(3, 'Maine Legends', 'Northeast');

INSERT INTO Beer (style, brewery, inventory, beer_Name, price, year)
VALUES (1, 1, 3000, 'Hopalicious', 1.5, 2020),
(2, 2, 2514, 'Lonesome Lager', 2, 2021),
(3, 3, 4567, 'Farmhouse Tankard', 1.3, 2022);

INSERT INTO Orders (customer, total_Sales, total_Beers, date)
VALUES (2, 19.39, 3, '2023-02-04 07:33:34'),
(3, 30.21, 6, '2023-02-20 09:26:09'),
(1, 125.28, 24, '2023-04-05 17:03:11'),
(3, 46.24, 8, '2023-06-08 12:09:18');

INSERT INTO Beer_Orders (sales_ID, product_ID, invoice_ID, quantity, total_Price)
VALUES (22, 3, 1, 2, 13.96),
(88, 2, 2, 2, 18.68),
(209, 1, 3, 6, 31.32),
(344, 1, 1, 4, 27.92);




