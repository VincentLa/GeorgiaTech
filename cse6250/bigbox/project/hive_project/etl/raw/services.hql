DROP TABLE IF EXISTS services;
CREATE EXTERNAL TABLE services (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    TRANSFERTIME TIMESTAMP,
    PREV_SERVICE VARCHAR(20),
    CURR_SERVICE VARCHAR(20)
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/services'
tblproperties ("skip.header.line.count"="1");
