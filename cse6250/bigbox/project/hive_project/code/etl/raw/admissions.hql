-- 1. sudo su - hdfs
-- hdfs dfs -mkdir -p /mimic/admissions
-- hdfs dfs -mkdir -p /mimic/callout
-- hdfs dfs -mkdir -p /mimic/caregivers
-- hdfs dfs -mkdir -p /mimic/chartevents
-- hdfs dfs -mkdir -p /mimic/cptevents
-- hdfs dfs -mkdir -p /mimic/datetimeevents
-- hdfs dfs -mkdir -p /mimic/diagnoses_icd
-- hdfs dfs -mkdir -p /mimic/drgcodes
-- hdfs dfs -mkdir -p /mimic/d_cpt
-- hdfs dfs -mkdir -p /mimic/d_icd_diagnoses
-- hdfs dfs -mkdir -p /mimic/d_icd_procedures
-- hdfs dfs -mkdir -p /mimic/d_items
-- hdfs dfs -mkdir -p /mimic/d_labitems
-- hdfs dfs -mkdir -p /mimic/icustays
-- hdfs dfs -mkdir -p /mimic/inputevents_cv
-- hdfs dfs -mkdir -p /mimic/inputevents_mv
-- hdfs dfs -mkdir -p /mimic/labevents
-- hdfs dfs -mkdir -p /mimic/microbiologyevents
-- hdfs dfs -mkdir -p /mimic/notevents
-- hdfs dfs -mkdir -p /mimic/outputevents
-- hdfs dfs -mkdir -p /mimic/outputevents


-- 3. hdfs dfs -chown -R root /mimic
-- 4. exit
-- 5. hdfs dfs -put  -f  /path-to-events.csv /input/events/

DROP TABLE IF EXISTS admissions;
CREATE EXTERNAL TABLE admissions (
  ROW_ID INT,
  SUBJECT_ID INT,
  HADM_ID INT,
  ADMITTIME TIMESTAMP,
  DISCHTIME TIMESTAMP,
  DEATHTIME TIMESTAMP,
  ADMISSION_TYPE VARCHAR(50),
  ADMISSION_LOCATION VARCHAR(50),
  DISCHARGE_LOCATION VARCHAR(50),
  INSURANCE VARCHAR(255),
  LANGUAGE VARCHAR(10),
  RELIGION VARCHAR(50),
  MARITAL_STATUS VARCHAR(50),
  ETHNICITY VARCHAR(200),
  EDREGTIME TIMESTAMP,
  EDOUTTIME TIMESTAMP,
  DIAGNOSIS VARCHAR(255),
  HOSPITAL_EXPIRE_FLAG SMALLINT,
  HAS_CHARTEVENTS_DATA SMALLINT
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/admissions'
tblproperties ("skip.header.line.count"="1");
