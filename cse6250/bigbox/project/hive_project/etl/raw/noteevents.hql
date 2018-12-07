-- awk '(NR-1)%2{$1=$1}1' RS=\" ORS=\" ./project/data/NOTEEVENTS.csv > /tmp/NOTEEVENTS.csv;  cp /tmp/NOTEEVENTS.csv ./project/data/NOTEEVENTS.csv
DROP TABLE IF EXISTS noteevents;
CREATE EXTERNAL TABLE noteevents (
    ROW_ID INT,
    SUBJECT_ID INT,
    HADM_ID INT,
    CHARTDATE TIMESTAMP,
    CHARTTIME TIMESTAMP,
    STORETIME TIMESTAMP,
    CATEGORY VARCHAR(50),
    DESCRIPTION VARCHAR(255),
    CGID INT,
    ISERROR VARCHAR(1),
    TEXT STRING
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/mimic/noteevents'
tblproperties ("skip.header.line.count"="1");
