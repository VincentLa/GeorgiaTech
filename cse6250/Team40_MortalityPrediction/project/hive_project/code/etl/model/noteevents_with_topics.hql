DROP TABLE IF EXISTS noteevents_with_topics;
CREATE EXTERNAL TABLE noteevents_with_topics (
    HADM_IDS INT,
    NOTEEVENT_ROW_ID INT,
    TOPIC_INDEXES INT,
    TOPIC_LABELS STRING,
    TOPIC_SCORES DOUBLE
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES (    "separatorChar" = ",",    "quoteChar"     = "\"" )
STORED AS TEXTFILE
LOCATION '/model/noteevents_with_topics'
tblproperties ("skip.header.line.count"="1");
