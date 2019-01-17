DROP TABLE IF EXISTS chartevents;
CREATE EXTERNAL TABLE chartevents (
  ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    ICUSTAY_ID INT,
    ITEMID INT,
    CHARTTIME TIMESTAMP,
    STORETIME TIMESTAMP,
    CGID INT,
    VALUE VARCHAR(255),
    VALUENUM DOUBLE,
    VALUEUOM VARCHAR(50),
    WARNING INT,
    ERROR INT,
    RESULTSTATUS VARCHAR(50),
    STOPPED VARCHAR(50)
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/chartevents'
tblproperties ("skip.header.line.count"="1");
