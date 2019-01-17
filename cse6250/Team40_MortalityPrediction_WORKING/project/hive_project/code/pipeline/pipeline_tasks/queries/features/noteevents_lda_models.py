"""
Take the Charts in Note Events and Perform Topic Modeling

Output the dictionary, lda_model, and lda_model_tfidf objects.
See LDA On Note Event Data Jupyter Notebook for development steps
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
import pickle
from pyhive import hive
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

# DWH = os.getenv('MIMIC_DWH')
# engine = create_engine(DWH)

pd.options.display.max_columns = 1000
pd.options.display.max_rows = 1000
pd.set_option('display.float_format', lambda x: '%.3f' % x)


# Currently set limit to 200,000 for just testing purposes. Will want to remove later.
QUERY = """
select
  subject_id,
  hadm_id,
  chartdate,
  text
from noteevents
--from mimiciii.noteevents
limit 200000
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

def process_docs(df):
    """
    Process Documents

    1. Tokenization: Split the text into sentences and the sentences into words. Lowercase the words and remove punctuation.
    2. Words that have fewer than 3 characters are removed.
    3. All stopwords are removed.
    4. Words are lemmatized — words in third person are changed to first person and verbs in past and future tenses are changed into present.
    5. Words are stemmed — words are reduced to their root form.
    """
    data_text = df[['text']]
    # print('printing text')
    # print(data_text)
    data_text['index'] = data_text.index
    documents = data_text
    processed_docs = documents['text'].map(preprocess)
    return processed_docs

def return_dictionary(processed_docs):
    """
    Create a dictionary from ‘processed_docs’ containing the number of times a word appears in the training set.

    Gensim filter_extremes:
        Filter out tokens that appear in less than 15 documents (absolute number) or
        more than 0.5 documents (fraction of total corpus size, not absolute number).
        after the above two steps, keep only the first 100000 most frequent tokens.
    """
    dictionary = gensim.corpora.Dictionary(processed_docs)
    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
    return dictionary

def run_lda(processed_docs, dictionary):
    """
    We run LDA using two methods:

    1. Bag of Words
    2. TF-IDF
    """
    # Bag of Words
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    lda_model = gensim.models.LdaMulticore(
        bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

    # TF-IDF
    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]
    lda_model_tfidf = gensim.models.LdaMulticore(
        corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)

    return lda_model, lda_model_tfidf


def main():
    """Execute Stuff"""
    print('Running noteevents_lda_models to perform topic modeling')
    args = get_args()
    # dbm = DBManager(db_url=args.db_url)

    print('Loading DataFrame')
    conn = hive.Connection(host='localhost', port=10000, auth='NOSASL')
    df = pd.read_sql(QUERY, conn)

    print('Successfully Loaded DataFrame, now running LDA!')
    processed_docs = process_docs(df)
    dictionary = return_dictionary(processed_docs)
    lda_model, lda_model_tfidf = run_lda(processed_docs, dictionary)

    print('Finished Running LDA! Now Writing objects to disk!')
    dictionary_pickle = open('./inventory/dictionary.obj', 'wb')
    lda_model_pickle = open('./inventory/lda_model.obj', 'wb')
    lda_model_tfidf_pickle = open('./inventory/lda_model_tfidf.obj', 'wb')

    pickle.dump(dictionary, dictionary_pickle)
    pickle.dump(lda_model, lda_model_pickle)
    pickle.dump(lda_model_tfidf, lda_model_tfidf_pickle)


if __name__ == '__main__':
    """
    See https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    main()
