DROP TABLE IF EXISTS prescriptions;
CREATE EXTERNAL TABLE prescriptions (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    ICUSTAY_ID INT,
    STARTDATE TIMESTAMP,
    ENDDATE TIMESTAMP,
    DRUG_TYPE VARCHAR(100),
    DRUG VARCHAR(100),
    DRUG_NAME_POE VARCHAR(100),
    DRUG_NAME_GENERIC VARCHAR(100),
    FORMULARY_DRUG_CD VARCHAR(120),
    GSN VARCHAR(200),
    NDC VARCHAR(120),
    PROD_STRENGTH VARCHAR(120),
    DOSE_VAL_RX VARCHAR(120),
    DOSE_UNIT_RX VARCHAR(120),
    FORM_VAL_DISP VARCHAR(120),
    FORM_UNIT_DISP VARCHAR(120),
    ROUTE VARCHAR(120)
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/prescriptions'
tblproperties ("skip.header.line.count"="1");
