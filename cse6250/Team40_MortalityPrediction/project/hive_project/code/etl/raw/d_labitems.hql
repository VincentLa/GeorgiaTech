DROP TABLE IF EXISTS d_labitems;
CREATE EXTERNAL TABLE d_labitems (
    ROW_ID INT,
    ITEMID INT,
    LABEL VARCHAR(100),
    FLUID VARCHAR(100),
    CATEGORY VARCHAR(100),
    LOINC_CODE VARCHAR(100)
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/d_labitems'
tblproperties ("skip.header.line.count"="1");
