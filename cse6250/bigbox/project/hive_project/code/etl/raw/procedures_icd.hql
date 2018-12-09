DROP TABLE IF EXISTS procedures_icd;
CREATE EXTERNAL TABLE procedures_icd (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    SEQ_NUM INT,
    ICD9_CODE VARCHAR(10)
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/procedures_icd'
tblproperties ("skip.header.line.count"="1");
