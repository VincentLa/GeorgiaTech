/*
   Phase 3 SQL Schema and Seed Data
   CS 6400 - Spring 2017
   Team 010
*/


DROP DATABASE IF EXISTS `cs6400_sp17_team010`;

SET default_storage_engine=InnoDB;

CREATE DATABASE IF NOT EXISTS cs6400_sp17_team010 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE cs6400_sp17_team010;

CREATE TABLE `User` (
  UserName varchar(30) NOT NULL,
  Email varchar(30) NOT NULL UNIQUE,
  `Password` varchar(30) NOT NULL,
  FirstName varchar(30) NOT NULL,
  LastName varchar(30) NOT NULL,
  SiteID int(16) unsigned NOT NULL,
  PRIMARY KEY (UserName)
);

CREATE TABLE Requests (
  UserName varchar(30) NOT NULL,
  RequestDateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ItemID int(16) unsigned NOT NULL,
  CountRequested smallint unsigned NOT NULL DEFAULT 0,
  CountProvided int(16) DEFAULT NULL,
  Status enum('Filled', 'Partially Filled', 'Unable to be Filled', 'Pending') DEFAULT 'Pending',
  PRIMARY KEY (UserName, RequestDateTime, ItemID)
);

CREATE TABLE Site (
  SiteID int(16) unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  StreetAddress varchar(100) NOT NULL,
  City varchar(50) NOT NULL,
  `State` varchar(2) NOT NULL,
  ZipCode varchar(5) NOT NULL,
  PrimaryPhone varchar(12) NOT NULL,
  PRIMARY KEY (SiteID)
);

CREATE TABLE FoodBank (
  ServiceID int(16) unsigned NOT NULL AUTO_INCREMENT,
  SiteID int(16) unsigned NOT NULL UNIQUE,
  PRIMARY KEY (ServiceID)
);

CREATE TABLE Shelter (
  ServiceID int(16) unsigned NOT NULL AUTO_INCREMENT,
  RoomsAvailable smallint unsigned NOT NULL DEFAULT 0,
  `Name` varchar(100) NOT NULL,
  Address varchar(200) NOT NULL,
  HoursOfOperation varchar(255) NOT NULL,
  ConditionsForUse varchar(255) NOT NULL,
  SiteID int(16) unsigned NOT NULL UNIQUE,
  PRIMARY KEY (ServiceID)
);

CREATE TABLE SoupKitchen (
  ServiceID int(16) unsigned NOT NULL AUTO_INCREMENT,
  SeatsAvailable smallint unsigned NOT NULL DEFAULT 0,
  SeatCapacity smallint unsigned NOT NULL DEFAULT 0,
  `Name` varchar(100) NOT NULL,
  Address varchar(200) NOT NULL,
  HoursOfOperation varchar(255) NOT NULL,
  ConditionsForUse varchar(255) NOT NULL,
  SiteID int(16) unsigned NOT NULL UNIQUE,
  PRIMARY KEY (ServiceID)
);

CREATE TABLE FoodPantry (
  ServiceID int(16) unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  Address varchar(200) NOT NULL,
  HoursOfOperation varchar(255) NOT NULL,
  ConditionsForUse varchar(255) NOT NULL,
  SiteID int(16) unsigned NOT NULL UNIQUE,
  PRIMARY KEY (ServiceID)
);

CREATE TABLE Item (
  ItemID int(16) unsigned NOT NULL AUTO_INCREMENT,
  ItemType enum('Food', 'Supplies') NOT NULL,
  ItemSubType enum('Vegetables', 'Nuts/Grains/Beans', 'Meat/Seafood', 'Dairy/Eggs', 'Sauce/Condiment/Seasoning', 'Juice/Drink', 'Personal Hygiene', 'Clothing', 'Shelter', 'Other') NOT NULL,
  `Name` varchar(30) NOT NULL,
  NumberOfUnit smallint unsigned NOT NULL,
  UnitType enum('Bag', 'Box', 'Carton', 'Others') NOT NULL,
  ExpirationDate date DEFAULT '9999-01-01',
  StorageType enum('Dry Good', 'Refrigerated', 'Frozen') NOT NULL,
  ServiceID int(16) unsigned NOT NULL,
  PRIMARY KEY (ItemID)
);

CREATE TABLE FamilyRoom (
  RoomNumber int(16) unsigned NOT NULL,
  ServiceID int(16) unsigned NOT NULL,
  OccupationStatus boolean,
  PRIMARY KEY (RoomNumber, ServiceID)
);

CREATE TABLE BunkRoom (
  RoomNumber int(16) unsigned NOT NULL,
  ServiceID int(16) unsigned NOT NULL,
  BunksAvailable smallint unsigned NOT NULL,
  BunkCapacity smallint unsigned NOT NULL,
  BunkType enum('Male', 'Female', 'Mix') NOT NULL,
  PRIMARY KEY (RoomNumber, ServiceID)
);

CREATE TABLE WaitList (
  ServiceID int(16) unsigned NOT NULL,
  ClientID int(16) unsigned NOT NULL,
  WaitListPosition smallint unsigned NOT NULL,
  PRIMARY KEY (ServiceID, ClientID)
);

CREATE TABLE Client (
  ClientID int(16) unsigned NOT NULL AUTO_INCREMENT,
  IDDescription varchar(255) NOT NULL,
  IDNumber varchar(30) NOT NULL,
  FirstName varchar(30) NOT NULL,
  LastName varchar(30) NOT NULL,
  PhoneNumber varchar(12),
  PRIMARY KEY (ClientID)
);

CREATE TABLE Log (
  ClientID int(16) unsigned NOT NULL,
  LogDateTime timestamp DEFAULT CURRENT_TIMESTAMP,
  SiteName varchar(100) NOT NULL,
  ServiceDescription varchar(500) NOT NULL,
  Notes varchar(500),
  PRIMARY KEY (ClientID, LogDateTime)
);


--  Table Constraints

ALTER TABLE `User`
  ADD CONSTRAINT UserFK1 FOREIGN KEY (SiteID) REFERENCES Site (SiteID);

ALTER TABLE `Requests`
  ADD CONSTRAINT RequestsFK1 FOREIGN KEY (UserName) REFERENCES `User` (UserName) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT RequestsFK2 FOREIGN KEY (ItemID) REFERENCES `Item` (ItemID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `FoodBank`
  ADD CONSTRAINT FoodbankFK1 FOREIGN KEY (SiteID) REFERENCES Site (SiteID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Shelter`
  ADD CONSTRAINT ShelterFK1 FOREIGN KEY (SiteID) REFERENCES Site (SiteID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `SoupKitchen`
  ADD CONSTRAINT SoupKitchenFK1 FOREIGN KEY (SiteID) REFERENCES Site (SiteID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `FoodPantry`
  ADD CONSTRAINT FoodPantryFK1 FOREIGN KEY (SiteID) REFERENCES Site (SiteID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Item`
  ADD CONSTRAINT ItemFK1 FOREIGN KEY (ServiceID) REFERENCES FoodBank (ServiceID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `FamilyRoom`
  ADD CONSTRAINT FamilyRoomFK1 FOREIGN KEY (ServiceID) REFERENCES Shelter (ServiceID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `BunkRoom`
  ADD CONSTRAINT BunkRoomFK1 FOREIGN KEY (ServiceID) REFERENCES Shelter (ServiceID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `WaitList`
  ADD CONSTRAINT WaitListFK1 FOREIGN KEY (ServiceID) REFERENCES Shelter (ServiceID) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT WaitListFK2 FOREIGN KEY (ClientID) REFERENCES Client (ClientID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `Log`
  ADD CONSTRAINT LogFK1 FOREIGN KEY (ClientID) REFERENCES Client (ClientID) ON DELETE CASCADE ON UPDATE CASCADE;

-- Seed data

USE cs6400_sp17_team010;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE User;
TRUNCATE Site;
TRUNCATE FoodBank;
TRUNCATE Shelter;
TRUNCATE SoupKitchen;
TRUNCATE FoodPantry;
TRUNCATE Item;
TRUNCATE FamilyRoom;
TRUNCATE BunkRoom;
TRUNCATE Client;
TRUNCATE WaitList;
TRUNCATE Log;
TRUNCATE Requests;
SET FOREIGN_KEY_CHECKS = 1; 

INSERT INTO Site (Name, StreetAddress, City, State, ZipCode, PrimaryPhone)
VALUES
('Site1', '123 Street', 'Atlanta', 'GA', '95123', '678-555-1230'),
('Site2', '234 Street', 'Atlanta', 'GA', '94123', '678-555-2340'),
('Site3', '345 Street', 'Atlanta', 'GA', '95000', '678-555-3450');

INSERT INTO User
VALUES
('emp1', 'emp1@somemail.com', 'gatech123', 'Site1', 'Employee1', 1),
('emp2', 'emp2@somemail.com', 'gatech123', 'Site2', 'Employee2', 2),
('emp3', 'emp3@somemail.com', 'gatech123', 'Site3', 'Employee3', 3),
('vol1', 'vol1@somemail.com', 'gatech123', 'Site1', 'Volunteer1', 1),
('vol2', 'vol2@somemail.com', 'gatech123', 'Site2', 'Volunteer2', 2),
('vol3', 'vol3@somemail.com', 'gatech123', 'Site3', 'Volunteer3', 3);

INSERT INTO FoodBank (SiteID)
VALUES(1), (2), (3);

INSERT INTO Shelter (RoomsAvailable, Name, Address, HoursOfOperation, ConditionsForUse, SiteID)
VALUES
(0, 'shelter2', 'Suite 1', '7am-7pm everyday', 'An ID of any form is required', 2),
(0, 'shelter3', 'Suite 1', '7am-7pm everyday', 'An ID of any form is required', 3);

INSERT INTO SoupKitchen(SeatsAvailable, SeatCapacity, Name, Address, HoursOfOperation, ConditionsForUse, SiteID)
VALUES(100, 100, 'soup2', 'Suite 2', '7am-7pm everyday', 'An ID of any form is required', 2),
(100, 100, 'soup3', 'Suite 2', '7am-7pm everyday', 'No ID required', 3);

INSERT INTO FoodPantry(Name, Address, HoursOfOperation, ConditionsForUse, SiteID)
VALUES('pantry1', 'Suite 3', '9am-5pm Mon to Fri', 'User of system', 1),
('pantry3', 'Suite 3', '9am-5pm Mon to Sun', 'User of system', 3);

INSERT INTO Item(ItemType, ItemSubType, Name, NumberOfUnit, UnitType, ExpirationDate, StorageType, ServiceID)
VALUES
('Food', 'Vegetables', 'Spinach', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Spring Greens', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Cabbage', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Kale', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Lettuce', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Red Lettuce', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Chard', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Collard', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Watercress', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Vegetables', 'Radicchio', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Nuts/Grains/Beans', 'Salted Nuts', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Pine Nuts', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Chestnuts', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Mixed Nuts', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Walnuts', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Almonds', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Peanuts', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Cashews', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Macadamia Nuts', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Nuts/Grains/Beans', 'Pecans', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Tomato Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Basil Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Pesto Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'White Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Mustard', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Onion Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Garlic Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Barbecue Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Miso Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Sauce/Condiment/Seasoning', 'Soy Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Food', 'Juice/Drink','Shasta',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Fanta',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Grape Soda',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Lime Soda',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Lemon Soda',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Italian soda',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Apple Soda',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Sprite',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Coca Cola',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Juice/Drink','Cherry Pepsi',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Meat/Seafood','Beef',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Beef Tender',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Beef With Bones',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Beef Steak',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Beef Roast',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Beef Strips',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Beef Sirloin',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Ground Beef',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Ground Lamb',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Meat/Seafood','Ground Bison',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 1),
('Food', 'Dairy/Eggs','Cheddar',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','Parmesan',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','Gouda',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','Chevre',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','Wensleydale',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','Romano',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','Mozzarella',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','Swiss Cheese',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','Gruyere',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Food', 'Dairy/Eggs','American Cheese',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 1),
('Supplies', 'Personal Hygiene', 'Shampoo', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Personal Hygiene', 'Toothbrush', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Personal Hygiene', 'Toothpaste', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Personal Hygiene', 'Deodorant', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Personal Hygiene', 'Soap/Detergent', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Clothing', 'Shirt', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Clothing', 'Pants', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Clothing', 'Skirts', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Clothing', 'Coats', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),
('Supplies', 'Clothing', 'Underwear', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 1),

('Food', 'Vegetables', 'Baby Carrots', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Carrots', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Ginger', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Beets', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Potatoes', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Daikon Radish', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Parsnips', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Jicama', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Celery Root', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Vegetables', 'Sweet Potatoes', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Nuts/Grains/Beans', 'Rice', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Unbleached Flour', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Quick Oats', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Rye', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Wheat Germ', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Basmati Rice', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Wild Rice', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Rice Flour', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Corn Meal', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Nuts/Grains/Beans', 'Wheat Bulgur', 100, 'Bag', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Ketchup', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Mayonnaise', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Worcestershire Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Dill Relish', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Lime Pickle', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Sriracha Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Tabasco', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Hoisin Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Fish Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Sauce/Condiment/Seasoning', 'Plum Sauce', 100, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Food', 'Juice/Drink','Coconut Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Orange Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Wheatgrass Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Lime Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Lemon Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Grape Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Apple Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Peach Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Watermelon Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Juice/Drink','Cherry Juice',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Meat/Seafood','Shrimp',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Salmon',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Fish Sticks',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Cod',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Crab',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Fish Fillets',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Shrimp Scampi',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Tilapia',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Butterfly Shrimp',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Meat/Seafood','Flounder',100,'Bag',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Frozen', 2),
('Food', 'Dairy/Eggs','Brown Eggs',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','White Eggs',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','Quail Eggs',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','Goose Eggs',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','Quiche',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','Egg Whites',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','Egg Substitute',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','Organic Eggs',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','Free Range Eggs',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Food', 'Dairy/Eggs','Duck Eggs',100,'Box',CONCAT(CURDATE() + INTERVAL 10 DAY), 'Refrigerated', 2),
('Supplies', 'Shelter', 'Tent', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Shelter', 'Sleeping Bag', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Shelter', 'Blanket', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Shelter', 'Winter Jacket', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Shelter', 'Rain Coat', 150, 'Others', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Other', 'Paper Towels', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Other', 'Toilet Paper', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Other', 'Pet Food', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Other', 'Batteries', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),
('Supplies', 'Other', 'Napkins', 50, 'Box', CONCAT(CURDATE() + INTERVAL 10 DAY), 'Dry Good', 2),

('Food', 'Meat/Seafood','Chicken Wings',100,'Bag',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Meat/Seafood','Chicken Tenders',100,'Bag',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Meat/Seafood','Chicken Patties',100,'Bag',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Meat/Seafood','Ground Chicken',100,'Bag',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Meat/Seafood','Whole Chicken',100,'Bag',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Meat/Seafood','Cornish Hens',100,'Bag',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Dairy/Eggs','Whole Milk',100,'Box',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Dairy/Eggs','2% Milk',100,'Box',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Dairy/Eggs','1% Milk',100,'Box',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Dairy/Eggs','Half and Half',100,'Box',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Dairy/Eggs','Whipping Cream',100,'Box',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3),
('Food', 'Dairy/Eggs','Buttermilk',100,'Box',CONCAT(CURDATE() - INTERVAL 10 DAY), 'Refrigerated', 3);


INSERT INTO FamilyRoom -- RoomNumber, ServiceID, OccupationStatus
VALUES
    (1, 1, True),
    (2, 1, True),
    (3, 1, True),
    (4, 1, True),
    (5, 1, True),
    (6, 1, True),
    (7, 1, True),
    (1, 2, True),
    (2, 2, True),
    (3, 2, True),
    (4, 2, True),
    (5, 2, True);

INSERT INTO BunkRoom -- RoomNumber, ServiceID, BunksAvailable, BunkCapacity, BunkType
VALUES
    (1, 1, 4, 4, 'Male'),
    (2, 1, 4, 4, 'Female'),
    (3, 1, 4, 4, 'Mix'),
    (1, 2, 4, 4, 'Male'),
    (2, 2, 4, 4, 'Female'),
    (3, 2, 4, 4, 'Mix');

INSERT INTO Client(IDDescription, IDNumber, FirstName, LastName, PhoneNumber)
VALUES
    ('Driver License', 'DL111111', 'Joe', 'Client1', '678-555-1111'),
    ('Library Card', 'LC123456', 'Joe', 'Client2', NULL),
    ('Social Security', '555-55-5555', 'Joe', 'Client3', NULL),
    ('Driver License', 'DL222222', 'Joe', 'Client4', NULL),
    ('Driver License', 'DL333333', 'Joe', 'Client5', NULL),
    ('Library Card', 'LC222222', 'Joe', 'Client6', NULL),
    ('Driver License', 'DL444444', 'Jane', 'Client7', NULL),
    ('Driver License', 'DL555555', 'Jane', 'Client8', NULL),
    ('Social Security', '666-66-6666', 'Jane', 'Client9', NULL),
    ('Driver License', 'DL666666', 'Jane', 'Client10', NULL),
    ('Social Security', '666-66-6666', 'Jane', 'Client11', NULL),
    ('Driver License', 'DL666666', 'Jane', 'Client12', NULL);

INSERT INTO WaitList -- ServiceID, ClientID, WaitListPosition
VALUES
    (1, 1, 1),
    (1, 2, 2),
    (1, 3, 3),
    (1, 4, 4),
    (2, 5, 1),
    (2, 6, 2),
    (2, 7, 3),
    (2, 8, 4);

INSERT INTO Requests (UserName, ItemID, CountRequested)
VALUES
    ('emp1', 76, 5),
    ('emp1', 77, 5),
    ('emp1', 78, 5),
    ('emp1', 79, 5),
    ('emp1', 80, 5),
    ('emp1', 81, 5),
    ('emp1', 82, 5),
    ('emp1', 83, 5),
    ('emp1', 84, 5),
    ('emp1', 85, 5),
    ('emp1',141, 5),
    ('emp1',142, 5),
    ('emp1',143, 5),
    ('emp1',144, 5),
    ('emp2', 1, 5),
    ('emp2', 2, 5),
    ('emp2', 3, 5),
    ('emp2', 4, 5),
    ('emp2', 5, 5),
    ('emp2', 6, 5),
    ('emp2', 7, 5),
    ('emp2', 8, 5),
    ('emp2', 9, 5),
    ('emp2', 10, 5),
    ('emp2', 145, 5),
    ('emp2', 146, 5),
    ('emp2', 147, 5),
    ('emp2', 148, 5),
    ('emp2', 61, 5),
    ('emp2', 62, 5),
    ('emp2', 63, 5),
    ('emp2', 64, 5),
    ('emp2', 65, 5),
    ('emp2', 66, 5),
    ('emp2', 67, 5),
    ('emp3',1,5),
    ('emp3',2,5),
    ('emp3',3,5),
    ('emp3',4,5),
    ('emp3',5,5),
    ('emp3',71,5),
    ('emp3',72,5),
    ('emp3',73,5),
    ('emp3',74,5),
    ('emp3',75,5),
    ('emp3',61,5),
    ('emp3',62,5),
    ('emp3',63,5),
    ('emp3',64,5),
    ('emp3',65,5),
    ('emp3',66,5),
    ('emp3',67,5),    
    ('emp3',131,5),
    ('emp3',132,5),
    ('emp3',133,5),
    ('emp3',134,5),
    ('emp3',135,5),
    ('emp3',136,5),
    ('emp3',137,5);

INSERT INTO Requests (UserName, ItemID, CountRequested, CountProvided, RequestDateTime, Status)
VALUES
    ('emp1',71,5,5,'2017-03-15 11:12:58','Filled'),
    ('emp1',72,5,5,'2017-03-15 11:13:58','Filled'),
    ('emp1',73,5,5,'2017-03-15 11:14:58','Filled'),
    ('emp1',74,5,5,'2017-03-15 11:15:58','Filled'),
    ('emp2',1,5,5,'2017-03-15 11:12:58','Filled'),
    ('emp2',2,5,5,'2017-03-15 11:13:58','Filled'),
    ('emp2',3,5,5,'2017-03-15 11:14:58','Filled'),
    ('emp2',4,5,5,'2017-03-15 11:15:58','Filled'),
    ('emp3',1,5,5,'2017-03-15 11:12:58','Filled'),
    ('emp3',2,5,5,'2017-03-15 11:13:58','Filled'),
    ('emp3',3,5,5,'2017-03-15 11:14:58','Filled'),
    ('emp3',4,5,5,'2017-03-15 11:15:58','Filled');

INSERT INTO Requests (UserName, ItemID, CountRequested)
VALUES
    ('vol1', 76, 5),
    ('vol1', 77, 5),
    ('vol1', 78, 5),
    ('vol1', 79, 5),
    ('vol1', 80, 5),
    ('vol1', 81, 5),
    ('vol1', 82, 5),
    ('vol1', 83, 5),
    ('vol1', 84, 5),
    ('vol1', 85, 5),
    ('vol1',141, 5),
    ('vol1',142, 5),
    ('vol1',143, 5),
    ('vol1',144, 5),
    ('vol2', 1, 5),
    ('vol2', 2, 5),
    ('vol2', 3, 5),
    ('vol2', 4, 5),
    ('vol2', 5, 5),
    ('vol2', 6, 5),
    ('vol2', 7, 5),
    ('vol2', 8, 5),
    ('vol2', 9, 5),
    ('vol2', 10, 5),
    ('vol2', 145, 5),
    ('vol2', 146, 5),
    ('vol2', 147, 5),
    ('vol2', 148, 5),
    ('vol2', 61, 5),
    ('vol2', 62, 5),
    ('vol2', 63, 5),
    ('vol2', 64, 5),
    ('vol2', 65, 5),
    ('vol2', 66, 5),
    ('vol2', 67, 5),
    ('vol3',1,5),
    ('vol3',2,5),
    ('vol3',3,5),
    ('vol3',4,5),
    ('vol3',5,5),
    ('vol3',71,5),
    ('vol3',72,5),
    ('vol3',73,5),
    ('vol3',74,5),
    ('vol3',75,5),
    ('vol3',61,5),
    ('vol3',62,5),
    ('vol3',63,5),
    ('vol3',64,5),
    ('vol3',65,5),
    ('vol3',66,5),
    ('vol3',67,5),    
    ('vol3',131,5),
    ('vol3',132,5),
    ('vol3',133,5),
    ('vol3',134,5),
    ('vol3',135,5),
    ('vol3',136,5),
    ('vol3',137,5);

INSERT INTO Requests (UserName, ItemID, CountRequested, CountProvided, RequestDateTime, Status)
VALUES
    ('vol1',71,5,5,'2017-03-15 11:12:58','Filled'),
    ('vol1',72,5,5,'2017-03-15 11:13:58','Filled'),
    ('vol1',73,5,5,'2017-03-15 11:14:58','Filled'),
    ('vol1',74,5,5,'2017-03-15 11:15:58','Filled'),
    ('vol2',1,5,5,'2017-03-15 11:12:58','Filled'),
    ('vol2',2,5,5,'2017-03-15 11:13:58','Filled'),
    ('vol2',3,5,5,'2017-03-15 11:14:58','Filled'),
    ('vol2',4,5,5,'2017-03-15 11:15:58','Filled'),
    ('vol3',1,5,5,'2017-03-15 11:12:58','Filled'),
    ('vol3',2,5,5,'2017-03-15 11:13:58','Filled'),
    ('vol3',3,5,5,'2017-03-15 11:14:58','Filled'),
    ('vol3',4,5,5,'2017-03-15 11:15:58','Filled');

INSERT INTO Log(ClientID, LogDateTime, SiteName, ServiceDescription, Notes)
VALUES 
    (1,'2017-03-15 11:12:58','Site1','profile created','profile created'),
    (2,'2017-03-16 11:12:58','Site1','profile created','profile created'),
    (3,'2017-03-17 11:12:58','Site1','profile created','profile created'),
    (4,'2017-03-18 11:12:58','Site1','profile created','profile created'),
    (5,'2017-03-19 11:12:58','Site2','profile created','profile created'),
    (6,'2017-03-20 11:12:58','Site2','profile created','profile created'),
    (7,'2017-03-21 11:12:58','Site2','profile created','profile created'),
    (8,'2017-03-22 11:12:58','Site2','profile created','profile created'),
    (9,'2017-03-23 11:12:58','Site2','profile created','profile created'),
    (10,'2017-03-24 11:12:58','Site2','profile created','profile created'),
    (11,'2017-03-25 11:12:58','Site2','profile created','profile created'),
    (12,'2017-03-26 11:12:58','Site2','profile created','profile created'),
    (1,'2017-03-27 11:12:58','Site1','visited pantry1','food provided'),
    (2,'2017-03-28 11:12:58','Site1','visited pantry1','food provided'),
    (3,'2017-03-29 11:12:58','Site1','visited pantry1','food provided'),
    (4,'2017-03-30 11:12:58','Site1','visited pantry1','food provided'),
    (5,'2017-03-31 11:12:58','Site2','visited soup2','meal provided'),
    (6,'2017-04-01 11:12:58','Site2','visited soup2','meal provided'),
    (7,'2017-04-02 11:12:58','Site2','visited soup2','meal provided'),
    (8,'2017-04-03 11:12:58','Site2','visited soup2','meal provided'),
    (9,'2017-04-04 11:12:58','Site2','visited shelter2','sleep provided'),
    (10,'2017-04-05 11:12:58','Site2','visited shelter2','sleep provided'),
    (11,'2017-04-06 11:12:58','Site2','visited shelter2','sleep provided'),
    (12,'2017-04-07 11:12:58','Site2','visited shelter2','sleep provided'),
    (1,'2017-04-08 11:12:58','Site3','visited pantry3','food provided'),
    (2,'2017-04-09 11:12:58','Site3','visited pantry3','food provided'),
    (3,'2017-04-10 11:12:58','Site3','visited pantry3','food provided'),
    (4,'2017-04-11 10:11:58','Site3','visited pantry3','food provided'),
    (5,'2017-04-11 11:12:58','Site3','visited soup3','meal provided'),
    (6,'2017-04-11 11:13:58','Site3','visited soup3','meal provided'),
    (7,'2017-04-11 11:14:58','Site3','visited soup3','meal provided'),
    (8,'2017-04-11 11:15:58','Site3','visited soup3','meal provided'),
    (9,'2017-04-11 11:16:58','Site3','visited shelter3','sleep provided'),
    (10,'2017-04-12 11:11:58','Site3','visited shelter3','sleep provided'),
    (11,'2017-04-12 11:12:58','Site3','visited shelter3','sleep provided'),
    (12,'2017-04-12 11:13:58','Site3','visited shelter3','sleep provided');













