DROP TABLE IF EXISTS diagnoses_icd;
CREATE EXTERNAL TABLE diagnoses_icd (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    SEQ_NUM INT,
    ICD9_CODE VARCHAR(10)
  )
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/mimic/diagnoses_icd'
tblproperties ("skip.header.line.count"="1");
