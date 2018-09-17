-- ***************************************************************************
-- DO NOT modify the below provided framework and variable names/orders please
-- Loading Data:
-- create external table mapping for events.csv and mortality_events.csv

-- IMPORTANT NOTES:
-- You need to put events.csv and mortality.csv under hdfs directory 
-- '/input/events/events.csv' and '/input/mortality/mortality.csv'
-- 
-- To do this, run the following commands for events.csv, 
-- 1. sudo su - hdfs
-- 2. hdfs dfs -mkdir -p /input/events
-- 3. hdfs dfs -chown -R root /input
-- 4. exit
-- Initially, put sample events into events and mortality just to test and compare against expected/hive/statistics.txt
-- 5. hdfs dfs -put -f /homeworks/hw2/code/sample_test/sample_events.csv /input/events/events.csv
-- 5. hdfs dfs -put -f /homeworks/hw2/code/sample_test/sample_mortality.csv /input/mortality/mortality.csv
-- However, once we finish testing, we should put real data in.
-- 5. hdfs dfs -put -f /homeworks/hw2/data/events.csv /input/events/events.csv
-- 5. hdfs dfs -put -f /homeworks/hw2/data/mortality.csv /input/mortality/mortality.csv
-- Follow the same steps 1 - 5 for mortality.csv, except that the path should be 
-- '/input/mortality'

-- To run file: hive -f event_statistics.hql 
-- ***************************************************************************
-- create events table 
DROP TABLE IF EXISTS events;
CREATE EXTERNAL TABLE events (
  patient_id STRING,
  event_id STRING,
  event_description STRING,
  time DATE,
  value DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/input/events';

-- create mortality events table 
DROP TABLE IF EXISTS mortality;
CREATE EXTERNAL TABLE mortality (
  patient_id STRING,
  time DATE,
  label INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/input/mortality';

-- ******************************************************
-- Task 1:
-- By manipulating the above two tables, 
-- generate two views for alive and dead patients' events
-- ******************************************************
-- find events for alive patients
DROP VIEW IF EXISTS alive_events;
CREATE VIEW alive_events AS
SELECT
  events.patient_id,
  events.event_id,
  events.time,
  mortality.time as mortality_date,
  mortality.label as is_dead
FROM events
  LEFT JOIN mortality
    ON events.patient_id = mortality.patient_id
where mortality.patient_id is NULL
  AND events.time IS NOT NULL
  AND events.event_id IS NOT NULL
;


-- find events for dead patients
DROP VIEW IF EXISTS dead_events;
CREATE VIEW dead_events AS
SELECT
  events.patient_id,
  events.event_id,
  events.time,
  mortality.time as mortality_date,
  mortality.label as is_dead
FROM events
  LEFT JOIN mortality
    on events.patient_id = mortality.patient_id
where mortality.patient_id is not NULL
  AND events.time IS NOT NULL
  AND events.event_id IS NOT NULL
;


-- ************************************************
-- Task 2: Event count metrics
-- Compute average, min and max of event counts 
-- for alive and dead patients respectively  
-- ************************************************
-- alive patients
INSERT OVERWRITE LOCAL DIRECTORY 'event_count_alive'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  avg(event_count),
  min(event_count),
  max(event_count)
FROM
(
SELECT
  patient_id,
  count(event_id) as event_count
from alive_events
GROUP BY patient_id
) as sub
;


-- dead patients
INSERT OVERWRITE LOCAL DIRECTORY 'event_count_dead'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  avg(event_count),
  min(event_count),
  max(event_count)
FROM
(
SELECT
  patient_id,
  count(event_id) as event_count
from dead_events
GROUP BY patient_id
) as sub
;


-- ************************************************
-- Task 3: Encounter count metrics 
-- Compute average, min and max of encounter counts 
-- for alive and dead patients respectively
-- ************************************************
-- alive
INSERT OVERWRITE LOCAL DIRECTORY 'encounter_count_alive'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  avg(encounter_count),
  min(encounter_count),
  max(encounter_count)
FROM
(
SELECT
  patient_id,
  count(distinct time) as encounter_count
from alive_events
GROUP BY patient_id
) as sub
;


-- dead
INSERT OVERWRITE LOCAL DIRECTORY 'encounter_count_dead'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  avg(encounter_count),
  min(encounter_count),
  max(encounter_count)
FROM
(
SELECT
  patient_id,
  count(distinct time) as encounter_count
from dead_events
GROUP BY patient_id
) as sub
;


-- ************************************************
-- Task 4: Record length metrics
-- Compute average, median, min and max of record lengths
-- for alive and dead patients respectively
-- ************************************************
-- alive 
INSERT OVERWRITE LOCAL DIRECTORY 'record_length_alive'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  avg(record_length),
  percentile(record_length, 0.5),
  min(record_length),
  max(record_length)
FROM
(
SELECT
  patient_id,
  min(time) as first_event_date,
  max(time) as last_event_date,
  datediff(max(time), min(time)) as record_length
from alive_events
GROUP BY patient_id
) as sub
;


-- dead
INSERT OVERWRITE LOCAL DIRECTORY 'record_length_dead'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  avg(record_length),
  percentile(record_length, 0.5),
  min(record_length),
  max(record_length)
FROM
(
SELECT
  patient_id,
  min(time) as first_event_date,
  max(time) as last_event_date,
  datediff(max(time), min(time)) as record_length
from dead_events
GROUP BY patient_id
) as sub
;


-- ******************************************* 
-- Task 5: Common diag/lab/med
-- Compute the 5 most frequently occurring diag/lab/med
-- for alive and dead patients respectively
-- *******************************************
-- alive patients
---- diag
INSERT OVERWRITE LOCAL DIRECTORY 'common_diag_alive'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  event_id,
  count(*) AS diag_count
FROM alive_events
where substr(event_id, 0, 4) = 'DIAG'
group by event_id
order by diag_count desc
limit 5
;


---- lab
INSERT OVERWRITE LOCAL DIRECTORY 'common_lab_alive'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  event_id,
  count(*) AS diag_count
FROM alive_events
where substr(event_id, 0, 3) = 'LAB'
group by event_id
order by diag_count desc
limit 5
;


---- med
INSERT OVERWRITE LOCAL DIRECTORY 'common_med_alive'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  event_id,
  count(*) AS diag_count
FROM alive_events
where substr(event_id, 0, 4) = 'DRUG'
group by event_id
order by diag_count desc
limit 5
;


-- dead patients
---- diag
INSERT OVERWRITE LOCAL DIRECTORY 'common_diag_dead'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  event_id,
  count(*) AS diag_count
FROM dead_events
where substr(event_id, 0, 4) = 'DIAG'
group by event_id
order by diag_count desc
limit 5
;


---- lab
INSERT OVERWRITE LOCAL DIRECTORY 'common_lab_dead'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  event_id,
  count(*) AS diag_count
FROM dead_events
where substr(event_id, 0, 3) = 'LAB'
group by event_id
order by diag_count desc
limit 5
;


---- med
INSERT OVERWRITE LOCAL DIRECTORY 'common_med_dead'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
SELECT
  event_id,
  count(*) AS diag_count
FROM dead_events
where substr(event_id, 0, 4) = 'DRUG'
group by event_id
order by diag_count desc
limit 5
;









