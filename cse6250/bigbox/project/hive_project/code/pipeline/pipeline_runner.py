"""
Script to batch run tasks

Note that for Python Files with Hive we can do:
conn = hive.Connection(host='localhost', port=10000, auth='NOSASL')
db_url= 'hive://localhost:10000/default'
"""

import argparse

import subprocess

import datetime as dt

import pandas as pd
import os

from utilities import sql_utils
from utilities.db_manager import DBManager

from pandas.io.sql import SQLTable


RUNTIME_ID = str(dt.datetime.now())
SQL_PATH = os.path.join(os.path.dirname(__file__), 'pipeline_tasks')

# Initialize runtime tracking
starttime = dt.datetime.now()


def _execute_insert(self, conn, keys, data_iter):
    """Optional, but useful: helps Pandas write tables against Postgres much faster.
    See https://github.com/pydata/pandas/issues/8953 for more info
    """
    print("Using monkey-patched _execute_insert")
    data = [dict((k, v) for k, v in zip(keys, row)) for row in data_iter]
    conn.execute(self.insert_statement().values(data))

SQLTable._execute_insert = _execute_insert


def _str2bool(v):
    """Define a function that converts string to bool used in argparse"""
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_args():
    """Use argparse to parse command line arguments."""
    parser = argparse.ArgumentParser(description='Runner for tasks')
    parser.add_argument('--db_url',
                        help='Database url string to the db.',
                        type=str,
                        required=False,
                        default='hive://localhost:10000/default')
    parser.add_argument(
        '--run_parse',
        help='Values: True or False. If True: Run Parse tasks; If False: Do not run parse tasks',
        type=_str2bool,
        default='false',
        required=False
    )
    parser.add_argument('--runtime_id', help='Run Time ID', type=str, default=RUNTIME_ID)
    return parser.parse_args()


def run_files(dbm, files, db_url):
    """Given a list of SQL or Python Files, run tasks in order.

    Keyword arguments:
    dbm -- Database Manager Object to help us read/write queries to tables
    files -- List of files containing SQL queries to run against the DWH
    db_url -- DB URL to Database
    """

    localstarttime = dt.datetime.now()

    for file in files:
        print("Start running file {}".format(file))
        if file[-3:] == '.py':
            p = subprocess.Popen(['python3', '-m',
                                  'pipeline.pipeline_tasks.{}'.format(file[:-3]),
                                  '--db_url={}'.format(db_url)])
            p.communicate()
            print("Done running the python file {}".format(file))
        elif file[-4:] == '.hql':
            with open(file, 'r') as sql_file:
                hql_file = sql_file.read()
                dbm.write_query_table(hql_file)
            # p = subprocess.Popen(['hive', '-f', 'pipeline/pipeline_tasks/{}'.format(file)])
            # p.communicate()
            print("Done running the hive file {}".format(file))
        elif file[-3:] == '.sh':
            p = subprocess.Popen(['bash', '{}'.format(file)])
            p.communicate()
            print("Done running the bash script {}".format(file))
        localendtime = dt.datetime.now()
        localduration = localendtime - localstarttime
        print(localendtime)
        print('Runtime: ' + str(localduration))
        print('\n')
        localstarttime = localendtime


def main():
    """Main function to run tasks."""
    args = get_args()
    dbm = DBManager(db_url=args.db_url)
    print('\n' + '\n' + 'Started at ' + str(starttime))
    print('\n')

    # Define the list of tasks that are parse tasks
    parse_tasks = [
    ]

    # Define list of files you want to run
    tasks = [
        '../etl/raw/hdfs_setup.sh',
        '../etl/raw/admissions.hql',
        '../etl/raw/callout.hql',
        '../etl/raw/caregivers.hql',
        '../etl/raw/ccs_dx_map.hql',
        '../etl/raw/ccs_proc_map.hql',
        '../etl/raw/chartevents.hql',
        '../etl/raw/cptevents.hql',
        '../etl/raw/d_cpt.hql',
        '../etl/raw/d_icd_diagnoses.hql',
        '../etl/raw/d_icd_procedures.hql',
        '../etl/raw/d_items.hql',
        '../etl/raw/d_labitems.hql',
        '../etl/raw/datetimeevents.hql',
        '../etl/raw/diagnoses_icd.hql',
        '../etl/raw/drgcodes.hql',
        '../etl/raw/icustays.hql',
        '../etl/raw/inputevents_cv.hql',
        '../etl/raw/inputevents_mv.hql',
        '../etl/raw/labevents.hql',
        '../etl/raw/microbiologyevents.hql',
        '../etl/raw/noteevents.hql',
        '../etl/raw/outputevents.hql',
        '../etl/raw/patients.hql',
        '../etl/raw/prescriptions.hql',
        '../etl/raw/procedureevents_mv.hql',
        '../etl/raw/procedures_icd.hql',
        '../etl/raw/services.hql',
        '../etl/raw/transfers.hql',
        'queries.features.noteevents_lda_models.py',
        'queries.features.noteevents_with_topics.py',
        '../etl/model/noteevents_with_topics.hql',
        'queries/datasets/admissions_diagnoses_icd_ccs_mapping.hql',
        'queries.datasets.admissions_ccs_ohe.py',
        '../etl/model/admissions_ccs_ohe.hql',
        'queries.datasets.admissions_topic_scores.py',
        '../etl/model/admissions_topic_scores.hql',
        'queries/datasets/model_demog.hql',
        'queries/datasets/model_demog_dx.hql',
        'queries/datasets/model_demog_dx_notetopics.hql',
    ]

    if args.run_parse:
        files = parse_tasks + tasks
    else:
        files = tasks

    print('files are')
    print(files)
    # Run files
    run_files(dbm, files, args.db_url)

    endtime = dt.datetime.now()
    duration = endtime - starttime

    print('Ended at: ' + str(endtime))
    print('Total Runtime: ' + str(duration))
    print('Done!')
    print('\n')


if __name__ == '__main__':
    main()
