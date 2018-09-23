/*
 One team member will act as "Presenter" for the Phase 3 demo. 
 Use this during your demo (if needed) to show db updates after UI interaction. 
 During the 15-20-minute demo, have your UI next to your phpMyAdmin/pgAdmin query window open (side by side). 
 After every button click, show the update in the database directly- either by refreshing the tables or direct SELECT * query (shown below).
 The goal is to ensure your app works and the interaction between the UI and DB is correct for all queries. 
 Sequentially demonstrate that all functional requirements are met, practice prior to the demo to ensure your presenter does not run out of time.  Any functionality which is not covered or does not work (Error 500) during the demo will be counted as 'missing' with applicable point deductions.  
 Timeline: 
   ~0-15min Presenter performs UI/DB Demo
   ~15-20min Discuss 'Brag Feature'- whatever your app does well above the requirements (each member to answer)
   ~20-25min Presenter TA Questions
*/

SELECT * FROM userinterests; 

SELECT schoolname, yeargraduated FROM attend ORDER BY yeargraduated DESC;

SELECT employername, jobtitle FROM employment ORDER BY employername DESC;

SELECT firstname, lastname, sex, birthdate, currentcity, hometown FROM user INNER JOIN regularuser ON user.email = regularuser.email WHERE user.email = 'michael@bluthco.com';

SELECT firstname, lastname FROM user WHERE user.email = 'michael@bluthco.com';

SELECT firstname, lastname, hometown FROM user INNER JOIN regularuser on regularuser.email = user.email WHERE regularuser.email = 'jdoe@gatech.edu';

SELECT firstname, lastname, hometown, relationship, user.email FROM friendship INNER JOIN regularuser ON regularuser.email = friendship.friendemail INNER JOIN user ON user.email = regularuser.email WHERE friendship.email = 'michael@bluthco.com' AND dateconnected IS NOT NULL ORDER BY lastname, firstname;

