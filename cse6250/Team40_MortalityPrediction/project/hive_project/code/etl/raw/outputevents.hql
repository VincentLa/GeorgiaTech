DROP TABLE IF EXISTS outputevents;
CREATE EXTERNAL TABLE outputevents (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    ICUSTAY_ID INT,
    CHARTTIME TIMESTAMP,
    ITEMID INT,
    VALUE DOUBLE,
    VALUEUOM VARCHAR(30),
    STORETIME TIMESTAMP,
    CGID INT,
    STOPPED VARCHAR(30),
    NEWBOTTLE CHAR(1),
    ISERROR INT
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/outputevents'
tblproperties ("skip.header.line.count"="1");
