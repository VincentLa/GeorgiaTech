sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/admissions'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/callout'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/caregivers'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/chartevents'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/cptevents'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/datetimeevents'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/diagnoses_icd'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/drgcodes'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/d_cpt'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/d_icd_diagnoses'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/d_icd_procedures'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/d_items'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/d_labitems'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/icustays'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/inputevents_cv'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/inputevents_mv'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/labevents'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/microbiologyevents'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/noteevents'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/outputevents'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/patients'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/prescriptions'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/procedureevents_mv'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/procedures_icd'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/services'
sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/transfers'
sudo su hdfs -c 'hdfs dfs -mkdir -p /ccs/ccs_dx_map'
sudo su hdfs -c 'hdfs dfs -mkdir -p /ccs/ccs_proc_map'
sudo su hdfs -c 'hdfs dfs -mkdir -p /model/noteevents_with_topics'
sudo su hdfs -c 'hdfs dfs -mkdir -p /model/admissions_ccs_ohe'
sudo su hdfs -c 'hdfs dfs -mkdir -p /model/admissions_topic_scores'
sudo su hdfs -c 'hdfs dfs -chown -R root /mimic'
sudo su hdfs -c 'hdfs dfs -chown -R root /ccs'
sudo su hdfs -c 'hdfs dfs -chown -R root /model'


hdfs dfs -put  -f /project/data/ADMISSIONS.csv /mimic/admissions
hdfs dfs -put  -f /project/data/CALLOUT.csv /mimic/callout
hdfs dfs -put  -f /project/data/CAREGIVERS.csv /mimic/caregivers
hdfs dfs -put  -f /project/data/CHARTEVENTS.csv /mimic/chartevents
hdfs dfs -put  -f /project/data/CPTEVENTS.csv /mimic/cptevents
hdfs dfs -put  -f /project/data/DATETIMEEVENTS.csv /mimic/datetimeevents
hdfs dfs -put  -f /project/data/DIAGNOSES_ICD.csv /mimic/diagnoses_icd
hdfs dfs -put  -f /project/data/DRGCODES.csv /mimic/drgcodes
hdfs dfs -put  -f /project/data/D_CPT.csv /mimic/d_cpt
hdfs dfs -put  -f /project/data/D_ICD_DIAGNOSES.csv /mimic/d_icd_diagnoses
hdfs dfs -put  -f /project/data/D_ICD_PROCEDURES.csv /mimic/d_icd_procedures
hdfs dfs -put  -f /project/data/D_ITEMS.csv /mimic/d_items
hdfs dfs -put  -f  /project/data/D_LABITEMS.csv /mimic/d_labitems
hdfs dfs -put  -f /project/data/ICUSTAYS.csv /mimic/icustays
hdfs dfs -put  -f /project/data/INPUTEVENTS_CV.csv /mimic/inputevents_cv
hdfs dfs -put  -f /project/data/INPUTEVENTS_MV.csv /mimic/inputevents_mv
hdfs dfs -put  -f /project/data/LABEVENTS.csv /mimic/labevents
hdfs dfs -put  -f /project/data/MICROBIOLOGYEVENTS.csv /mimic/microbiologyevents
hdfs dfs -put  -f /project/data/NOTEEVENTS.csv /mimic/noteevents
hdfs dfs -put  -f /project/data/OUTPUTEVENTS.csv /mimic/outputevents
hdfs dfs -put  -f /project/data/PATIENTS.csv /mimic/patients
hdfs dfs -put  -f /project/data/PRESCRIPTIONS.csv /mimic/prescriptions
hdfs dfs -put  -f /project/data/PROCEDUREEVENTS_MV.csv /mimic/procedureevents_mv
hdfs dfs -put  -f /project/data/PROCEDURES_ICD.csv /mimic/procedures_icd
hdfs dfs -put  -f /project/data/SERVICES.csv /mimic/services
hdfs dfs -put  -f /project/data/TRANSFERS.csv /mimic/transfers
hdfs dfs -put  -f /project/data/ccs/ccs_dx_map.csv /ccs/ccs_dx_map
hdfs dfs -put  -f /project/data/ccs/ccs_proc_map.csv /ccs/ccs_proc_map
hdfs dfs -put  -f /project/hive_project/code/inventory/noteevents_with_topics.csv /model/noteevents_with_topics
hdfs dfs -put  -f /project/hive_project/code/inventory/admissions_ccs_ohe.csv /model/admissions_ccs_ohe
hdfs dfs -put  -f /project/hive_project/code/inventory/admissions_topic_scores.csv /model/admissions_topic_scores
