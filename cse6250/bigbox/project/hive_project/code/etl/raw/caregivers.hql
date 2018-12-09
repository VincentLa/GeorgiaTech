DROP TABLE IF EXISTS caregivers;
CREATE EXTERNAL TABLE caregivers (
    ROW_ID INT ,
    CGID INT ,
    LABEL VARCHAR(15),
    DESCRIPTION VARCHAR(30)
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/caregivers'
tblproperties ("skip.header.line.count"="1");
