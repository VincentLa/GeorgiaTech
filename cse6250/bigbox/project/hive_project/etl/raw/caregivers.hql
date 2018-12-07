DROP TABLE IF EXISTS caregivers;
CREATE EXTERNAL TABLE caregivers (
    ROW_ID INT ,
    CGID INT ,
    LABEL VARCHAR(15),
    DESCRIPTION VARCHAR(30)
  )
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/mimic/caregivers'
tblproperties ("skip.header.line.count"="1");
