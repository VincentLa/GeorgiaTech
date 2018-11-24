"""
Load CCS Map for Diagnosis Codes

Source of data: https://www.hcup-us.ahrq.gov/toolssoftware/ccs/ccs.jsp
"""
import argparse
import glob
import os

import pandas as pd
import sqlalchemy as sa

from utilities.db_manager import DBManager
from utilities import util_functions as uf


def get_args():
    """Use argparse to parse command line arguments."""
    parser = argparse.ArgumentParser(description='Runner for tasks')
    parser.add_argument('--db_url', help='Database url string to the db.', required=True)
    return parser.parse_args()


def load_datasets(dbm, direc):
    """Data SF Campaign Finance Data

    Keyword Args:
        dbm: DBManager object
        dir: Directory where files are
    """
    extension = 'csv'
    filenames = os.listdir(direc)
    files = [filename for filename in filenames if filename.endswith(extension)]
    dx_file = [f for f in files if 'dx' in f]
    proc_file = [f for f in files if 'proc' in f]

    column_map = {
        'ICD-9-CM CODE': 'icd9cm_code',
        'CCS CATEGORY': 'ccs_category',
        'CCS CATEGORY DESCRIPTION': 'ccs_category_description',
        'ICD-9-CM CODE DESCRIPTION': 'icd9cm_code_description',
        'OPTIONAL CCS CATEGORY': 'optional_ccs_category',
        'OPTIONAL CCS CATEGORY DESCRIPTION': 'optional_ccs_category_description',
    }

    # Reading and Writing Candidate Files
    dfs = []
    for f in dx_file:
        print('Reading file {} into pandas.'.format(f))
        df = pd.read_csv(os.path.join(direc, f))
        df.rename(index=str, columns=column_map, inplace=True)
        dfs.append(df)

    print('Writing DX files into database.')
    df = pd.concat(dfs, ignore_index=True)
    dbm.write_df_table(
        df,
        table_name='ccs_icd9cm_map',
        schema='ontologies')

    # Reading and Writing Other Files
    dfs = []
    for f in proc_file:
        print('Reading file {} into pandas.'.format(f))
        df = pd.read_csv(os.path.join(direc, f))
        df.rename(index=str, columns=column_map, inplace=True)
        dfs.append(df)

    print('Writing other files into database.')
    df = pd.concat(dfs, ignore_index=True)
    dbm.write_df_table(
        df,
        table_name='ccs_icd9proc_map',
        schema='ontologies')


def main():
    """Execute Stuff"""
    print('Parsing and Loading MapLight California Bulk Data Sets')
    args = get_args()
    dbm = DBManager(db_url=args.db_url)
    git_root_dir = uf.get_git_root(os.path.dirname(__file__))
    directory = os.path.join(git_root_dir, 'cse6250', 'bigbox', 'project', 'data', 'ccs')
    load_datasets(dbm, directory)


if __name__ == '__main__':
    """See https://stackoverflow.com/questions/419163/what-does-if-name-main-do"""
    main()

