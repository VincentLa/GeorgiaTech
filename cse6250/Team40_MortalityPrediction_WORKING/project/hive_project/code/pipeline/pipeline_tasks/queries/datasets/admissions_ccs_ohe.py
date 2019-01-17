"""
Take CCS Categories for each Admission and perform One Hot Encoding
"""
import argparse
import os

import pandas as pd
from pyhive import hive
from sklearn.preprocessing import LabelBinarizer
import sqlalchemy as sa
from sqlalchemy import create_engine

from utilities.db_manager import DBManager
from utilities import util_functions as uf

# DWH = os.getenv('MIMIC_DWH')
# engine = create_engine(DWH)

QUERY = """
select
  hadm_id,
  ccs_category_description
from admissions_diagnoses_icd_ccs_mapping
where ccs_category_description is not null
"""


def get_args():
    """Use argparse to parse command line arguments."""
    parser = argparse.ArgumentParser(description='Runner for tasks')
    parser.add_argument('--db_url', help='Database url string to the db.', required=True)
    return parser.parse_args()


def perform_ohe():
    """
    Perform One Hot Encoding
    """
    conn = hive.Connection(host='localhost', port=10000, auth='NOSASL')
    df = pd.read_sql(QUERY, conn)
    print('printing dataframe')
    print(df.head())

    ccs_lb = LabelBinarizer()
    X = ccs_lb.fit_transform(df.ccs_category_description.values)

    # Perform One Hot Encoding
    adm_dx_one_hot = pd.DataFrame(
        X, columns=["ccs_" + str(int(i)) for i in range(X.shape[1])])
    df_adm_dx_one_hot = pd.concat([df, adm_dx_one_hot], axis=1)

    # Group at adm_idx level
    df_adm_dx_ohe = df_adm_dx_one_hot.groupby('hadm_id').max()
    df_adm_dx_ohe.reset_index(inplace=True)

    return df_adm_dx_ohe


def main():
    """Execute Stuff"""
    print('Running admissions_ccs_ohe.py. This file performs One Hot Encoding for Admissions and Diagnoses with Higher Level categorization with CCS Codes')
    args = get_args()
    # dbm = DBManager(db_url=args.db_url)

    df = perform_ohe()
    df.to_csv('./inventory/admissions_ccs_ohe.csv', index=False)


if __name__ == '__main__':
    """
    See https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    main()
