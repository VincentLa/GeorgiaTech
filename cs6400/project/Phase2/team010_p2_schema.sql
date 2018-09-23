/* 
   Phase 2 SQL Schema
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
  RoomNumber int(16) unsigned NOT NULL UNIQUE,
  ServiceID int(16) unsigned NOT NULL,
  OccupationStatus boolean,
  PRIMARY KEY (RoomNumber, ServiceID)
);

CREATE TABLE BunkRoom (
  RoomNumber int(16) unsigned NOT NULL UNIQUE,
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
  ClientID int(16) unsigned NOT NULL AUTO_INCREMENT,
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
