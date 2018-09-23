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
Note: key constraints will fail if order is not correct: order of statements matters! 
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


-- Constraints 

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


-- Insert Test (seed) Data 

-- Insert into user
-- example of using a hashsed password 'michael123' = $2y$08$kr5P80A7RyA0FDPUa8cB2eaf0EqbUay0nYspuajgHRRXM9SgzNgZO
-- depends on if you are storing the hash $storedHash or plaintext $storedPassword in login.php
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('admin@gtonline.com', 'admin123', 'Johnny', 'Admin');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('dschrute@dundermifflin.com', 'dwight123', 'Dwight', 'Schrute');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('gbluth@bluthco.com', 'george123', 'George', 'Bluth');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('jhalpert@dundermifflin.com', 'jim123', 'Jim', 'Halpert');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('lfunke@bluthco.com', 'lindsey123', 'Lindsey', 'Funke');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('michael@bluthco.com', 'michael123', 'Michael', 'Bluth');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('pam@dundermifflin.com', 'pam123', 'Pam', 'Halpert');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('tsmith@gatech.edu', 'tsmith123', 'Tom', 'Smith');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('jdoe@gatech.edu', 'jdoe123', 'Jane', 'Doe');
INSERT INTO `user` (email, `password`, firstname, lastname) VALUES('rocky@cc.gatech.edu', 'rocky123', 'Rocky', 'Dunlap');

-- Insert into adminuser
INSERT INTO adminuser (email, lastlogin) VALUES('admin@gtonline.com', NOW() );

-- Insert into regularuser
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('dschrute@dundermifflin.com', 'M', '1971-07-15', 'Scranton', 'Rochester');
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('gbluth@bluthco.com', 'M', '1950-11-17', 'Los Angeles', 'Los Angeles');
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('jhalpert@dundermifflin.com', 'M', '1973-10-02', 'Scranton', 'Buffalo');
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('lfunke@bluthco.com', 'F', '1974-05-05', 'Los Angeles', 'Las Vegas');
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('michael@bluthco.com', 'M', '1971-01-01', 'Phoenix', 'Beverly Hills');
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('pam@dundermifflin.com', 'F', '1975-04-28', 'Scranton', 'Sacramento');
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('rocky@cc.gatech.edu', 'M', '1981-03-22', 'Atlanta', 'Conyers');
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('tsmith@gatech.edu', 'M', '1980-01-12', 'Denver', 'Portland');
INSERT INTO regularuser (email, sex, birthdate, currentcity, hometown) VALUES('jdoe@gatech.edu', 'F', '1975-07-22', 'New York', 'Denver');

-- Insert into statusupdate
INSERT INTO statusupdate (email, dateandtime, `text`) VALUES('michael@bluthco.com', concat(CURDATE()-INTERVAL 3 MONTH,' 11:20:00'), 'My first status update!');
INSERT INTO statusupdate (email, dateandtime, `text`) VALUES('michael@bluthco.com', concat(CURDATE()-INTERVAL 2 MONTH,' 13:40:00'), 'Going to the store.');
INSERT INTO statusupdate (email, dateandtime, `text`) VALUES('rocky@cc.gatech.edu', concat(NOW()-INTERVAL 10 DAY), 'Going to a concert!');

-- Insert into comment
INSERT INTO `comment` (email, dateandtime, `text`, suemail, sudateandtime) VALUES('dschrute@dundermifflin.com', concat(CURDATE()-INTERVAL 3 MONTH,' 09:30:00'), 'Hi Dwight!', 'michael@bluthco.com', concat(CURDATE()-INTERVAL 3 MONTH,' 11:20:00'));
INSERT INTO `comment` (email, dateandtime, `text`, suemail, sudateandtime) VALUES('rocky@cc.gatech.edu', concat(CURDATE()-INTERVAL 3 MONTH,' 10:30:00'), 'Hi Rocky!', 'michael@bluthco.com', concat(CURDATE()-INTERVAL 2 MONTH,' 13:40:00') );

-- Insert into userinterests
INSERT INTO userinterests (email, interest) VALUES('jhalpert@dundermifflin.com', 'bird watching');
INSERT INTO userinterests (email, interest) VALUES('michael@bluthco.com', 'golf');
INSERT INTO userinterests (email, interest) VALUES('michael@bluthco.com', 'indie rock music');
INSERT INTO userinterests (email, interest) VALUES('michael@bluthco.com', 'swimming');
INSERT INTO userinterests (email, interest) VALUES('tsmith@gatech.edu', 'gaming');
INSERT INTO userinterests (email, interest) VALUES('tsmith@gatech.edu', 'hiking');
INSERT INTO userinterests (email, interest) VALUES('pam@dundermifflin.com', 'horse racing');
INSERT INTO userinterests (email, interest) VALUES('pam@dundermifflin.com', 'volleyball');
INSERT INTO userinterests (email, interest) VALUES('rocky@cc.gatech.edu', 'piano');
INSERT INTO userinterests (email, interest) VALUES('rocky@cc.gatech.edu', 'Per Nørgård');
INSERT INTO userinterests (email, interest) VALUES('rocky@cc.gatech.edu', 'classical music');
INSERT INTO userinterests (email, interest) VALUES('rocky@cc.gatech.edu', 'Copenhagen Opera House');
INSERT INTO userinterests (email, interest) VALUES('lfunke@bluthco.com', 'skydiving');
INSERT INTO userinterests (email, interest) VALUES('lfunke@bluthco.com', 'base jumping');
INSERT INTO userinterests (email, interest) VALUES('jdoe@gatech.edu', 'eating smørrebrød');
INSERT INTO userinterests (email, interest) VALUES('jdoe@gatech.edu', 'football (soccer)');

-- Insert into friendship
INSERT INTO friendship (email, friendemail, relationship, dateconnected) VALUES('michael@bluthco.com', 'gbluth@bluthco.com', 'Father', concat(CURDATE()-INTERVAL 10 YEAR));
INSERT INTO friendship (email, friendemail, relationship, dateconnected) VALUES('michael@bluthco.com', 'jhalpert@dundermifflin.com', 'Long Lost Cousin', NULL);
INSERT INTO friendship (email, friendemail, relationship, dateconnected) VALUES('michael@bluthco.com', 'lfunke@bluthco.com', 'Sister', concat(CURDATE()-INTERVAL 180 DAY));
INSERT INTO friendship (email, friendemail, relationship, dateconnected) VALUES('pam@dundermifflin.com', 'michael@bluthco.com', 'Colleague', NULL);
INSERT INTO friendship (email, friendemail, relationship, dateconnected) VALUES('tsmith@gatech.edu', 'michael@bluthco.com', 'Boss', NULL);
INSERT INTO friendship (email, friendemail, relationship, dateconnected) VALUES('rocky@cc.gatech.edu', 'michael@bluthco.com', 'Peer', concat(CURDATE()-INTERVAL 5 MONTH));
INSERT INTO friendship (email, friendemail, relationship, dateconnected) VALUES('michael@bluthco.com', 'rocky@cc.gatech.edu', 'Peer', concat(CURDATE()-INTERVAL 8 YEAR));

-- Insert into employer
INSERT INTO employer (employername) VALUES('Bluth Development Company');
INSERT INTO employer (employername) VALUES('Dunder Mifflin');
INSERT INTO employer (employername) VALUES('Georgia Institute of Technology');

-- Insert into employment
INSERT INTO employment (email, employername, jobtitle) VALUES('dschrute@dundermifflin.com', 'Dunder Mifflin', 'Student Intern');
INSERT INTO employment (email, employername, jobtitle) VALUES('michael@bluthco.com', 'Bluth Development Company', 'Software Developer I');
INSERT INTO employment (email, employername, jobtitle) VALUES('rocky@cc.gatech.edu', 'Georgia Institute of Technology', 'Teaching Assistant');

-- Insert into schooltype
INSERT INTO schooltype (typename) VALUES('Community College');
INSERT INTO schooltype (typename) VALUES('High School');
INSERT INTO schooltype (typename) VALUES('University');

-- Insert into school
INSERT INTO school (schoolname, `type`) VALUES('Phoenix High School', 'High School');
INSERT INTO school (schoolname, `type`) VALUES('Pikes Peak Community College', 'Community College');
INSERT INTO school (schoolname, `type`) VALUES('University of Georgia', 'University');
INSERT INTO school (schoolname, `type`) VALUES('University of California', 'University');
INSERT INTO school (schoolname, `type`) VALUES('University of Colorado', 'University');
INSERT INTO school (schoolname, `type`) VALUES('Georgia Institute of Technology', 'University');

-- Insert into attend
INSERT INTO attend (email, schoolname, yeargraduated) VALUES('michael@bluthco.com', 'Phoenix High School', 1989);
INSERT INTO attend (email, schoolname, yeargraduated) VALUES('michael@bluthco.com', 'University of California', 1993);
INSERT INTO attend (email, schoolname, yeargraduated) VALUES('michael@bluthco.com', 'Georgia Institute of Technology', 2016);
INSERT INTO attend (email, schoolname, yeargraduated) VALUES('rocky@cc.gatech.edu', 'Pikes Peak Community College', 1993);
INSERT INTO attend (email, schoolname, yeargraduated) VALUES('rocky@cc.gatech.edu', 'University of Colorado', 1996);
INSERT INTO attend (email, schoolname, yeargraduated) VALUES('rocky@cc.gatech.edu', 'Georgia Institute of Technology', 2016);