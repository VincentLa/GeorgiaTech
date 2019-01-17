DROP TABLE IF EXISTS d_icd_diagnoses;
CREATE EXTERNAL TABLE d_icd_diagnoses (
    ROW_ID INT,
    ICD9_CODE VARCHAR(10),
    SHORT_TITLE VARCHAR(50),
    LONG_TITLE VARCHAR(255)
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/d_icd_diagnoses'
tblproperties ("skip.header.line.count"="1");
