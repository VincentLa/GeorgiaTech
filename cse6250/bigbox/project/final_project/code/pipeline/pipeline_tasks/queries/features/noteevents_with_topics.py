"""
Take the dictionary, lda_model, and lda_model_tfidf objects produced by noteevents_lda_models and
label each note in noteevents and write to DB.

See LDA On Note Event Data Jupyter Notebook for development steps
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
import pickle
import sqlalchemy as sa
from sqlalchemy import create_engine

sys.path.append('../')
from utilities import sql_utils as su
from utilities import model_eval_utils as meu
from utilities.db_manager import DBManager

# Import Packages for NLP
import gensim
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
# import nltk.stem as stemmer
import numpy as np
np.random.seed(2018)
import nltk
nltk.download('wordnet')

stemmer = SnowballStemmer('english')

DWH = os.getenv('MIMIC_DWH')
engine = create_engine(DWH)

pd.options.display.max_columns = 1000
pd.options.display.max_rows = 1000
pd.set_option('display.float_format', lambda x: '%.3f' % x)


# Currently set limit to 1,000 for just testing purposes. Will want to remove later.
QUERY = """
select
  subject_id,
  hadm_id,
  row_id,
  chartdate,
  text
from mimiciii.noteevents
where hadm_id is not null
limit 1000
"""


def get_args():
    """Use argparse to parse command line arguments."""
    parser = argparse.ArgumentParser(description='Runner for tasks')
    parser.add_argument('--db_url', help='Database url string to the db.', required=True)
    return parser.parse_args()

def label_charts_with_topics(dictionary, lda_model, lda_model_tfidf):
    """
    Write Topics to DB

    Loop through each chart and label with topics.
    """
    dict_topic_score = {}
    hadm_ids = []
    texts = []
    text_ids = []
    topic_indexes = []
    topic_scores = []
    topic_labels = []
    for idx, row in df.iterrows():
        chart = row['text']
        bow_vector = dictionary.doc2bow(preprocess(chart))
        for topic_index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
            hadm_ids.append(row['hadm_id'])
            texts.append(row['text'])
            text_ids.append(row['row_id'])
            topic_indexes.append(topic_index)
            topic_scores.append(score)
            topic_labels.append(lda_model.print_topic(topic_index, 5))
    dict_topic_score['hadm_ids'] = hadm_ids
    dict_topic_score['texts'] = texts
    dict_topic_score['text_ids'] = text_ids
    dict_topic_score['topic_indexes'] = topic_indexes
    dict_topic_score['topic_scores'] = topic_scores
    dict_topic_score['topic_labels'] = topic_labels

    df_topic_score = pd.DataFrame(dict_topic_score)
    print(df_topic_score.head())
    print(df_topic_score.shape)

    return df_topic_score


def main():
    """Execute Stuff"""
    print('Running noteevents_lda_models to perform topic modeling')
    args = get_args()
    dbm = DBManager(db_url=args.db_url)

    print('DataFrame')
    df = dbm.load_query_table(QUERY)

    print('Loading Dictionary, and LDA Model Objects!')
    dictionary_pickle = open('./inventory/dictionary.obj', 'r')
    lda_model_pickle = open('./inventory/lda_model.obj', 'r')
    lda_model_tfidf_pickle = open('./inventory/lda_model_tfidf.obj', 'r')

    dictionary = pickle.load(dictionary_pickle)
    lda_model = pickle.load(lda_model_pickle)
    lda_model_tfidf = pickle.load(lda_model_tfidf_pickle)

    print('Using LDA Model Objects to Label Notes!')
    df_topic_score = label_charts_with_topics(dictionary, lda_model, lda_model_tfidf)


if __name__ == '__main__':
    """
    See https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    main()
