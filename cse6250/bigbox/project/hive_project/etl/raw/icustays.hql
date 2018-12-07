DROP TABLE IF EXISTS icustays;
CREATE EXTERNAL TABLE icustays (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    ICUSTAY_ID INT,
    DBSOURCE VARCHAR(20),
    FIRST_CAREUNIT VARCHAR(20),
    LAST_CAREUNIT VARCHAR(20),
    FIRST_WARDID SMALLINT,
    LAST_WARDID SMALLINT,
    INTIME TIMESTAMP,
    OUTTIME TIMESTAMP,
    LOS DOUBLE
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/icustays'
tblproperties ("skip.header.line.count"="1");
