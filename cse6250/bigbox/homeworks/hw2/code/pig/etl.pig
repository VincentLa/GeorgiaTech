-- ***************************************************************************
-- TASK
-- Aggregate events into features of patient and generate training, testing data for mortality prediction.
-- Steps have been provided to guide you.
-- You can include as many intermediate steps as required to complete the calculations.
-- To run pig: pig -x local
-- Note to cleanup before run; bash tmp/clean_pig.sh
-- ***************************************************************************

-- ***************************************************************************
-- TESTS
-- To test, please change the LOAD path for events and mortality to ../../test/events.csv and ../../test/mortality.csv
-- 6 tests have been provided to test all the subparts in this exercise.
-- Manually compare the output of each test against the csv's in test/expected folder.
-- ***************************************************************************

-- register a python UDF for converting data into SVMLight format
REGISTER utils.py USING jython AS utils;

-- load events file
-- events = LOAD '../../data/events.csv' USING PigStorage(',') AS (patientid:int, eventid:chararray, eventdesc:chararray, timestamp:chararray, value:float);
events = LOAD '../sample_test/sample_events.csv' USING PigStorage(',') AS (patientid:int, eventid:chararray, eventdesc:chararray, timestamp:chararray, value:float);

-- select required columns from events
events = FOREACH events GENERATE patientid, eventid, ToDate(timestamp, 'yyyy-MM-dd') AS etimestamp, value;

-- load mortality file
-- mortality = LOAD '../../data/mortality.csv' USING PigStorage(',') as (patientid:int, timestamp:chararray, label:int);
mortality = LOAD '../sample_test/sample_mortality.csv' USING PigStorage(',') as (patientid:int, timestamp:chararray, label:int);

mortality = FOREACH mortality GENERATE patientid, ToDate(timestamp, 'yyyy-MM-dd') AS mtimestamp, label;

--To display the relation, use the dump command e.g. DUMP mortality;

-- ***************************************************************************
-- Compute the index dates for dead and alive patients
-- ***************************************************************************
eventswithmort = JOIN events BY patientid LEFT OUTER, mortality by patientid; -- perform join of events and mortality by patientid;

-- detect the events of dead patients and create it of the form (patientid, eventid, value, label, time_difference) where time_difference is the days between index date and each event timestamp
deadevents = FILTER eventswithmort BY label == 1; 
deadevents = FOREACH deadevents GENERATE events::patientid as patientid, events::eventid as eventid, events::value as value, events::etimestamp as etimestamp, mortality::label as label, SubtractDuration(mortality::mtimestamp, 'P30D') as index_date;
deadevents = FOREACH deadevents GENERATE patientid, eventid, value, label, DaysBetween(index_date, etimestamp) as time_difference;

-- detect the events of alive patients and create it of the form (patientid, eventid, value, label, time_difference) where time_difference is the days between index date and each event timestamp
aliveevents = FILTER eventswithmort BY label is null;
aliveevents = FOREACH aliveevents GENERATE events::patientid as patientid, events::eventid as eventid, events::etimestamp as etimestamp, events::value as value; 

---- Find Last Event Date for each Alive Patient
ae_patients = GROUP aliveevents by patientid;
ae_patients_max_date = FOREACH ae_patients GENERATE group as patientid, MAX(aliveevents.etimestamp) as max_event_date;
  
---- Join back to get the latest event date for each patient
aliveevents = JOIN aliveevents BY patientid LEFT OUTER, ae_patients_max_date by patientid;
aliveevents = FOREACH aliveevents GENERATE aliveevents::patientid as patientid, aliveevents::eventid as eventid, aliveevents::etimestamp as etimestamp, aliveevents::value as value, ae_patients_max_date::max_event_date as index_date; 
aliveevents = FOREACH aliveevents GENERATE patientid, eventid, value, 0 as label, DaysBetween(index_date, etimestamp) as time_difference;


--TEST-1
deadevents = ORDER deadevents BY patientid, eventid;
aliveevents = ORDER aliveevents BY patientid, eventid;
STORE aliveevents INTO 'aliveevents' USING PigStorage(',');
STORE deadevents INTO 'deadevents' USING PigStorage(',');

-- ***************************************************************************
-- Filter events within the observation window and remove events with missing values
-- ***************************************************************************
allevents = union aliveevents, deadevents;
allevents = FILTER allevents BY value is not null;
filtered = FILTER allevents by time_difference <= 2000; -- contains only events for all patients within the observation window of 2000 days and is of the form (patientid, eventid, value, label, time_difference)

--TEST-2
filteredgrpd = GROUP filtered BY 1;
filtered = FOREACH filteredgrpd GENERATE FLATTEN(filtered);
filtered = ORDER filtered BY patientid, eventid, time_difference;
STORE filtered INTO 'filtered' USING PigStorage(',');

-- ***************************************************************************
-- Aggregate events to create features
-- ***************************************************************************
by_patients_eventid = GROUP filtered BY (patientid, eventid);

-- for group of (patientid, eventid), count the number of  events occurred for the patient and create relation of the form (patientid, eventid, featurevalue)
featureswithid = FOREACH by_patients_eventid GENERATE
  FLATTEN(group) as (patientid, eventid),
  COUNT(filtered) as featurevalue;

--TEST-3
featureswithid = ORDER featureswithid BY patientid, eventid;
STORE featureswithid INTO 'features_aggregate' USING PigStorage(',');

-- ***************************************************************************
-- Generate feature mapping
-- ***************************************************************************
by_events = GROUP featureswithid BY eventid; 
distinct_events = FOREACH by_events GENERATE
  FLATTEN(group) as eventid,
  COUNT(featureswithid) as temp_count;
distinct_events = FOREACH distinct_events GENERATE eventid;
distinct_events = ORDER distinct_events BY eventid;
ranked_events = rank distinct_events by eventid asc;

-- compute the set of distinct eventids obtained from previous step, sort them by eventid and then rank these features by eventid to create (idx, eventid). Rank should start from 0.
all_features = FOREACH ranked_events GENERATE rank_distinct_events - 1 as idx, eventid;

-- store the features as an output file
STORE all_features INTO 'features' using PigStorage(' ');

-- perform join of featureswithid and all_features by eventid and replace eventid with idx. It is of the form (patientid, idx, featurevalue)
features = JOIN featureswithid BY eventid LEFT OUTER, all_features by eventid;
features = FOREACH features GENERATE featureswithid::patientid as patientid, all_features::idx as idx, featureswithid::featurevalue as featurevalue;

--TEST-4
features = ORDER features BY patientid, idx;
STORE features INTO 'features_map' USING PigStorage(',');

-- ***************************************************************************
-- Normalize the values using min-max normalization
-- Use DOUBLE precision
-- ***************************************************************************
by_idx = GROUP features BY idx;
-- group events by idx and compute the maximum feature value in each group. I t is of the form (idx, maxvalue)
maxvalues = FOREACH by_idx GENERATE
  FLATTEN(group) as idx,
  MAX(features.featurevalue) as maxvalue;

-- join features and maxvalues by idx
normalized = JOIN features by idx LEFT OUTER, maxvalues by idx;
normalized = FOREACH normalized GENERATE features::patientid as patientid, features::idx as idx, features::featurevalue as featurevalue, maxvalues::maxvalue as maxvalue;

-- compute the final set of normalized features of the form (patientid, idx, normalizedfeaturevalue)
features = FOREACH normalized GENERATE patientid, idx, 1.0 * featurevalue / maxvalue as normalizedfeaturevalue;

--TEST-5
features = ORDER features BY patientid, idx;
STORE features INTO 'features_normalized' USING PigStorage(',');

-- ***************************************************************************
-- Generate features in svmlight format
-- features is of the form (patientid, idx, normalizedfeaturevalue) and is the output of the previous step
-- e.g.  1,1,1.0
--  	 1,3,0.8
--	     2,1,0.5
--       3,3,1.0
-- ***************************************************************************

grpd = GROUP features BY patientid;
grpd_order = ORDER grpd BY $0;
features = FOREACH grpd_order
{
    sorted = ORDER features BY idx;
    generate group as patientid, utils.bag_to_svmlight(sorted) as sparsefeature;
}

-- ***************************************************************************
-- Split into train and test set
-- labels is of the form (patientid, label) and contains all patientids followed by label of 1 for dead and 0 for alive
-- e.g. 1,1
--	2,0
--      3,1
-- ***************************************************************************

labels = -- create it of the form (patientid, label) for dead and alive patients

--Generate sparsefeature vector relation
samples = JOIN features BY patientid, labels BY patientid;
samples = DISTINCT samples PARALLEL 1;
samples = ORDER samples BY $0;
samples = FOREACH samples GENERATE $3 AS label, $1 AS sparsefeature;

--TEST-6
STORE samples INTO 'samples' USING PigStorage(' ');

-- randomly split data for training and testing
DEFINE rand_gen RANDOM('6505');
samples = FOREACH samples GENERATE rand_gen() as assignmentkey, *;
SPLIT samples INTO testing IF assignmentkey <= 0.20, training OTHERWISE;
training = FOREACH training GENERATE $1..;
testing = FOREACH testing GENERATE $1..;

-- save training and tesing data
STORE testing INTO 'testing' USING PigStorage(' ');
STORE training INTO 'training' USING PigStorage(' ');
