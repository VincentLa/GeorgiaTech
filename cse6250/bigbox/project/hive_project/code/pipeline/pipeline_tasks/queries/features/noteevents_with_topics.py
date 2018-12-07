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


# Can set limit e.g. 1,000 for just testing purposes. But remove the limit in production
QUERY = """
select
  subject_id,
  hadm_id,
  row_id,
  chartdate,
  text
from mimiciii.noteevents
where hadm_id is not null
"""


def get_args():
    """Use argparse to parse command line arguments."""
    parser = argparse.ArgumentParser(description='Runner for tasks')
    parser.add_argument('--db_url', help='Database url string to the db.', required=True)
    return parser.parse_args()

def lemmatize_stemming(text):
    """
    Lemmatize: lemmatized — words in third person are changed to first person
    
    Verbs in past and future tenses are changed into present.
    """
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


def preprocess(text):
    """
    Preprocess Text:
    
    Remove words in "STOPWORDS" and remove words 3 letters or less
    """
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

def label_charts_with_topics(df, dictionary, lda_model, lda_model_tfidf):
    """
    Write Topics to DB

    Keyword Args:
      df: DataFrame containing Charts (most likely from mimiciii.noteevents)
      dictionary: Dictionary Object Returned by LDA
      lda_model: LDA Model from Bag of Words
      lda_model_tf_idf: LDA Model from TF-IDF

    Loop through each chart and label with topics.
    """
    dict_topic_score = {}
    hadm_ids = []
    # texts = []
    text_ids = []
    topic_indexes = []
    topic_scores = []
    topic_labels = []
    for idx, row in df.iterrows():
        chart = row['text']
        bow_vector = dictionary.doc2bow(preprocess(chart))
        for topic_index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
            hadm_ids.append(row['hadm_id'])
            # texts.append(row['text'])
            text_ids.append(row['row_id'])
            topic_indexes.append(topic_index)
            topic_scores.append(score)
            topic_labels.append(lda_model.print_topic(topic_index, 5))
    dict_topic_score['hadm_ids'] = hadm_ids
    # dict_topic_score['texts'] = texts
    dict_topic_score['noteevent_row_id'] = text_ids
    dict_topic_score['topic_indexes'] = topic_indexes
    dict_topic_score['topic_scores'] = topic_scores
    dict_topic_score['topic_labels'] = topic_labels

    df_topic_score = pd.DataFrame(dict_topic_score)

    print('just printing dataframe to make sure it worked')
    print(df_topic_score.head())
    print(df_topic_score.shape)

    return df_topic_score


def main():
    """Execute Stuff"""
    print('Running noteevents_with_topics to read model objects and label note events')
    args = get_args()
    dbm = DBManager(db_url=args.db_url)

    print('Loading DataFrame')
    df = dbm.load_query_table(QUERY)

    print('Loading Dictionary, and LDA Model Objects!')
    dictionary_pickle = open('./inventory/dictionary.obj', 'rb')
    lda_model_pickle = open('./inventory/lda_model.obj', 'rb')
    lda_model_tfidf_pickle = open('./inventory/lda_model_tfidf.obj', 'rb')

    dictionary = pickle.load(dictionary_pickle)
    lda_model = pickle.load(lda_model_pickle)
    lda_model_tfidf = pickle.load(lda_model_tfidf_pickle)

    print('Using LDA Model Objects to Label Notes!')
    df_topic_score = label_charts_with_topics(df, dictionary, lda_model, lda_model_tfidf)

    print('Done Labeling Notes! Now saving the DF Locally just in case write to DB Fails')
    noteevents_with_topics_df_pickle = open('./inventory/noteevents_with_topics_df.obj', 'wb')
    pickle.dump(df_topic_score, noteevents_with_topics_df_pickle)
    
    print('Finally, writing to DB!')
    dbm.write_df_table(
        df_topic_score,
        table_name='noteevents_with_topics',
        schema='features',
        if_exists='replace',
        use_fast=True)

    print('Done Writing to DB!')


if __name__ == '__main__':
    """
    See https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    main()
