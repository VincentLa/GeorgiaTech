/*
CS6400 students are expected to write their own SQL. 
Note: if your SQL script is a dump (auto generated via phpMyAdmin/Workbench export), there will be ZERO points awarded for that portion of the submission.
Please change the team number below to reflect your correct team number including the leading zero. 

Project db: A relational db is required: teams are free to use PostgreSQL or MySQL if desired.  (Non-relational noSQL: Hadoop, Cassandra,  MongoDB, etc. are not allowed)
https://dev.mysql.com/doc/refman/5.7/en/introduction.html
https://www.postgresql.org/docs/9.6/static/index.html
The limited GT Online example below assumes a team will use MySQL. 
Note: we may run your PostgreSQL or MySQL script to see if it creates your schema successfully via phpMyAdmin/PgAdmin import, if not, point deductions may apply. 
*/

DROP DATABASE IF EXISTS `cs6400_sp17_team001`; 
/* 
Optional: MySQL centric items 
MySQL: DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
MySQL Storage Engines: SET default_storage_engine=InnoDB;
Note: "IF EXISTS" is not universal, and the "IF NOT EXISTS" is uncommonly supported, so this functionaly may not work if outside MySQL RDBMS.

Resources:
http://www.w3schools.com/
http://www.agiledata.org/essays/keys.html
https://dev.mysql.com/doc/refman/5.7/en/data-types.html
https://bitnami.com/stacks/infrastructure
https://www.jetbrains.com/phpstorm/
https://v4-alpha.getbootstrap.com/components/forms/
http://www.cs.montana.edu/~halla/csci440/index.html
https://lagunita.stanford.edu/courses/Engineering/db/2014_1/about
http://web.stanford.edu/class/cs145/
*/

SET default_storage_engine=InnoDB;

CREATE DATABASE IF NOT EXISTS cs6400_sp17_team001 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE cs6400_sp17_team001;

-- Tables 

CREATE TABLE adminuser (
  `admin_id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  email varchar(250) NOT NULL,
  lastlogin datetime DEFAULT NULL,
  PRIMARY KEY (admin_id), 
  UNIQUE KEY `email` (`email`)
);

CREATE TABLE `user` (
  `user_id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  email varchar(250) NOT NULL,
  `password` varchar(50) NOT NULL,
  firstname varchar(100) NOT NULL,
  lastname varchar(100) NOT NULL,
  PRIMARY KEY (user_id),
  UNIQUE KEY `email` (`email`)
);

CREATE TABLE regularuser (
  `reguser_id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  email varchar(250) NOT NULL,
  birthdate date NOT NULL,
  sex char(1) NULL,
  currentcity varchar(250) DEFAULT NULL,
  hometown varchar(250) DEFAULT NULL,
  PRIMARY KEY (reguser_id),
  UNIQUE KEY `email` (`email`)
);

CREATE TABLE `comment` (
  email varchar(250) NOT NULL,
  dateandtime datetime NOT NULL,
  `text` varchar(1000) NOT NULL,
  suemail varchar(250) NOT NULL,
  sudateandtime datetime NOT NULL,
  PRIMARY KEY (email,dateandtime),
  KEY suemail (suemail,sudateandtime)
);

CREATE TABLE statusupdate (
  email varchar(250) NOT NULL,
  dateandtime datetime NOT NULL,
  `text` varchar(1000) NOT NULL,
  PRIMARY KEY (email,dateandtime),
  KEY dateandtime (dateandtime)
);

CREATE TABLE userinterests (
  email varchar(250) NOT NULL,
  interest varchar(250) NOT NULL,
  PRIMARY KEY (email,interest)
);

CREATE TABLE friendship (
  email varchar(250) NOT NULL,
  friendemail varchar(250) NOT NULL,
  relationship varchar(50) NOT NULL,
  dateconnected date DEFAULT NULL,
  PRIMARY KEY (email,friendemail),
  KEY friendemail (friendemail)
);

CREATE TABLE employer (
  employername varchar(50) NOT NULL,
  PRIMARY KEY (employername)
);

CREATE TABLE employment (
  email varchar(250) NOT NULL,
  employername varchar(50) NOT NULL,
  jobtitle varchar(50) NOT NULL,
  PRIMARY KEY (email,employername),
  KEY employername (employername)
);

CREATE TABLE school (
  schoolname varchar(250) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (schoolname),
  KEY `type` (`type`)
);

CREATE TABLE schooltype (
  typename varchar(50) NOT NULL,
  PRIMARY KEY (typename)
);

CREATE TABLE attend (
  email varchar(250) NOT NULL,
  schoolname varchar(250) NOT NULL,
  yeargraduated int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (email,schoolname,yeargraduated),
  KEY schoolname (schoolname)
);


--  Table Constraints 

ALTER TABLE `adminuser`
  ADD CONSTRAINT adminuser_ibfk_1 FOREIGN KEY (email) REFERENCES `user` (email);
  
ALTER TABLE `regularuser`
  ADD CONSTRAINT regularuser_ibfk_1 FOREIGN KEY (email) REFERENCES `user` (email);

ALTER TABLE `statusupdate`
  ADD CONSTRAINT statusupdate_ibfk_1 FOREIGN KEY (email) REFERENCES regularuser (email);

 ALTER TABLE `comment`
  ADD CONSTRAINT comment_ibfk_1 FOREIGN KEY (suemail, sudateandtime) REFERENCES statusupdate (email, dateandtime);  

ALTER TABLE `userinterests`
  ADD CONSTRAINT userinterests_ibfk_1 FOREIGN KEY (email) REFERENCES regularuser (email);

ALTER TABLE `friendship`
  ADD CONSTRAINT friendship_ibfk_1 FOREIGN KEY (email) REFERENCES regularuser (email) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT friendship_ibfk_2 FOREIGN KEY (friendemail) REFERENCES regularuser (email) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `employment`
  ADD CONSTRAINT employment_ibfk_1 FOREIGN KEY (email) REFERENCES regularuser (email),
  ADD CONSTRAINT employment_ibfk_2 FOREIGN KEY (employername) REFERENCES employer (employername);

ALTER TABLE `school`
  ADD CONSTRAINT school_ibfk_1 FOREIGN KEY (`type`) REFERENCES schooltype (typename);

ALTER TABLE `attend`
  ADD CONSTRAINT attend_ibfk_1 FOREIGN KEY (email) REFERENCES regularuser (email),
  ADD CONSTRAINT attend_ibfk_2 FOREIGN KEY (schoolname) REFERENCES school (schoolname);
