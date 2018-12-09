import datetime

import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator

DAG_ARGS = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(hours=1),
}

PROJECT_DAG = DAG(
    dag_id='final_project',
    default_args=DAG_ARGS,
    schedule_interval=datetime.timedelta(hours=1)
)

SENTINEL_START = DummyOperator(
    task_id='sentinel_start',
    dag=PROJECT_DAG
)


MIMIC_ETL_FILES = [
    'admissions',
    'callout',
    'caregivers',
    'chartevents',
    'cptevents',
    'datetimeevents',
    'diagnoses_icd',
    'drgcodes',
    'd_cpt'
    'd_icd_diagnoses',
    'd_icd_procedures',
    'd_items',
    'd_labitems',
    'icustays',
    'inputevents_cv',
    'inputevents_mv',
    'labevents',
    'microbiologyevents',
    'noteevents',
    'outputevents',
    'patients',
    'prescriptions',
    'procedureevents_mv',
    'procedures_icd',
    'services',
    'transfers',
]


CCS_ETL_FILES = [
    'ccs_dx_map',
    'ccs_proc_map',
]

SENTINEL_INIT_ETL_END = DummyOperator(
    task_id='sentinel_init_etl_end',
    dag=PROJECT_DAG
)

for etl_set in {MIMIC_ETL_FILES, CCS_ETL_FILES}:
    for elem in etl_set:
        mkdir_op = BashOperator(
            task_id=f'mkdir_mimic_{elem}',
            bash_command=f"sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/{elem}'",
            dag=PROJECT_DAG
        )
        mkdir_op.set_upstream(SENTINEL_START)

        put_op = BashOperator(
            task_id=f'put_mimic_{elem}',
            bash_command=f"sudo su hdfs -c ' hdfs dfs -mkdir -p /mimic/{elem}'",
            dag=PROJECT_DAG
        )
        put_op.set_upstream(mkdir_op)
        put_op.set_downstream(SENTINEL_INIT_ETL_END)



# sudo su hdfs -c 'hdfs dfs -mkdir -p /model/noteevents_with_topics'
# sudo su hdfs -c 'hdfs dfs -mkdir -p /model/admissions_ccs_ohe'
# sudo su hdfs -c 'hdfs dfs -mkdir -p /model/admissions_topic_scores'
# sudo su hdfs -c 'hdfs dfs -chown -R root /mimic'
# sudo su hdfs -c 'hdfs dfs -chown -R root /ccs'
# sudo su hdfs -c 'hdfs dfs -chown -R root /model'
# ]

if __name__ == "__main__":
    PROJECT_DAG.cli()
