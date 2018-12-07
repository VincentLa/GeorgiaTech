DROP TABLE IF EXISTS drgcodes;
CREATE EXTERNAL TABLE drgcodes (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    DRG_TYPE VARCHAR(20),
    DRG_CODE VARCHAR(20),
    DESCRIPTION VARCHAR(255),
    DRG_SEVERITY SMALLINT,
    DRG_MORTALITY SMALLINT,
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/drgcodes'
tblproperties ("skip.header.line.count"="1");
