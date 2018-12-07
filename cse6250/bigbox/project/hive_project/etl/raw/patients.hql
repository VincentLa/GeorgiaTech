DROP TABLE IF EXISTS patients;
CREATE EXTERNAL TABLE patients (
    ROW_ID INT,
    SUBJECT_ID INT,
    GENDER VARCHAR(5),
    DOB TIMESTAMP,
    DOD TIMESTAMP,
    DOD_HOSP TIMESTAMP,
    DOD_SSN TIMESTAMP,
    EXPIRE_FLAG INT
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/patients'
tblproperties ("skip.header.line.count"="1");
