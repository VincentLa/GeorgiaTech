"""
Takes Topics Produced by LDA Models for and creates features for each topic for the admission.

That is, each row is unique at the admission level with columns with the sum of scores for each
topic from documents pertaining to that admission.
"""
import argparse
import os

import pandas as pd
from sklearn.preprocessing import LabelBinarizer
import sqlalchemy as sa
from sqlalchemy import create_engine

from utilities.db_manager import DBManager
from utilities import util_functions as uf

DWH = os.getenv('MIMIC_DWH')
engine = create_engine(DWH)

QUERY = """
select
  hadm_ids,
  topic_indexes,
  sum(topic_scores) as topic_scores
from features.noteevents_with_topics
group by hadm_ids, topic_indexes
"""


def get_args():
    """Use argparse to parse command line arguments."""
    parser = argparse.ArgumentParser(description='Runner for tasks')
    parser.add_argument('--db_url', help='Database url string to the db.', required=True)
    return parser.parse_args()


def create_adm_topic_features():
    """
    Creates Features given DataFrame unique at the hadm_id and topic_indexes level.

    Basically need to pivot to get unique at hadm_ids level.
    """
    with engine.begin() as conn:
        df = pd.read_sql(QUERY, conn)
    df_pivoted = df.pivot(index='hadm_ids', columns='topic_indexes', values='topic_scores')
    df_pivoted.columns = ['topic_' + str(col) for col in df_pivoted.columns.values]
    df_pivoted.reset_index(inplace=True)
    df_pivoted.fillna(0, inplace=True)

    print('printing Pivoted Dataset head just to check it works')
    print(df_pivoted.head())
    print(df_pivoted.shape)
    return df_pivoted    


def main():
    """Execute Stuff"""
    print('Running admissions_topic_scores.py')
    args = get_args()
    dbm = DBManager(db_url=args.db_url)

    print('Loading DataFrame')
    df = create_adm_topic_features()
    
    print('Successfully Loaded DataFrame now writing to DB!')
    dbm.write_df_table(
        df,
        table_name='admissions_topic_scores',
        schema='datasets',
        if_exists='replace')


if __name__ == '__main__':
    """
    See https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    main()
