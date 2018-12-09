DROP TABLE IF EXISTS admissions_topic_scores;
CREATE EXTERNAL TABLE admissions_topic_scores (
    HADM_IDS INT,
    TOPIC_0 DOUBLE,
    TOPIC_1 DOUBLE,
    TOPIC_2 DOUBLE,
    TOPIC_3 DOUBLE,
    TOPIC_4 DOUBLE,
    TOPIC_5 DOUBLE,
    TOPIC_6 DOUBLE,
    TOPIC_7 DOUBLE,
    TOPIC_8 DOUBLE,
    TOPIC_9 DOUBLE
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/model/admissions_topic_scores'
tblproperties ("skip.header.line.count"="1");
