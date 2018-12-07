DROP TABLE IF EXISTS transfers;
CREATE EXTERNAL TABLE transfers (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    ICUSTAY_ID INT,
    DBSOURCE VARCHAR(20),
    EVENTTYPE VARCHAR(20),
    PREV_CAREUNIT VARCHAR(20),
    CURR_CAREUNIT VARCHAR(20),
    PREV_WARDID SMALLINT,
    CURR_WARDID SMALLINT,
    INTIME TIMESTAMP,
    OUTTIME TIMESTAMP,
    LOS DOUBLE
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
   "separatorChar" = ",",
   "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION '/mimic/transfers'
tblproperties ("skip.header.line.count"="1");
