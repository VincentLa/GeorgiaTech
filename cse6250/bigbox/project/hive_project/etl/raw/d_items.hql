DROP TABLE IF EXISTS d_items;
CREATE EXTERNAL TABLE d_items (
    ROW_ID INT,
    ITEMID INT,
    LABEL VARCHAR(200),
    ABBREVIATION VARCHAR(100),
    DBSOURCE VARCHAR(20),
    LINKSTO VARCHAR(50),
    CATEGORY VARCHAR(100),
    UNITNAME VARCHAR(100),
    PARAM_TYPE VARCHAR(30),
    CONCEPTID INT
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/d_items'
tblproperties ("skip.header.line.count"="1");
