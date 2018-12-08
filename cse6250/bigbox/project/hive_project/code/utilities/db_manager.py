"""Creating a class that will manage interactions with Postgres Database"""
import urllib.parse

import pandas as pd
import pyhive
import psycopg2 as ps
import sqlalchemy as sa
from pandas.io.sql import SQLTable

from utilities.util_functions import df_to_sql


def _execute_insert(self, conn, keys, data_iter):
    """Optional, but useful: helps Pandas write tables against Postgres much faster.
    See https://github.com/pydata/pandas/issues/8953 for more info
    """
    print("Using monkey-patched _execute_insert")
    data = [dict((k, v) for k, v in zip(keys, row)) for row in data_iter]
    conn.execute(self.insert_statement().values(data))

SQLTable._execute_insert = _execute_insert


class DBManager(object):

    def __init__(self, db_url):
        self.db_url = db_url
        result = urllib.parse.urlparse(db_url)
        self.host = result.hostname
        self.port = result.port
        self.user = result.username
        self.dbname = result.path[1:]
        self.password = result.password
        self.engine = sa.create_engine(db_url)

    def create_schema(self, schema):
        """Creates schema if does not exist"""
        conn_string = "host={0} user={1} dbname={2} password={3}".format(
            self.host, self.user, self.dbname, self.password)
        conn = ps.connect(conn_string)
        with conn:
            cur = conn.cursor()
            query = 'CREATE SCHEMA IF NOT EXISTS {schema};'.format(schema=schema)
            cur.execute(query)

    def load_table(self, table_name, schema):
        """Reads Table and stores in a Pandas Dataframe"""
        with self.engine.begin() as conn:
            df = pd.read_sql_table(table_name=table_name, con=conn, schema=schema)
            return df

    def load_query_table(self, query):
        """Reads a SQL Query and stores in a Pandas Dataframe"""
        with self.engine.begin() as conn:
            df = pd.read_sql(query, conn)
            return df

    def write_query_table(self, query):
        """Given a Create Table Query. Execute the Query to write against the DWH"""
        conn=hive.Connection(host=self.host, port=self.port,auth='NOSASL')
        conn.execute(query) 

    def write_df_table(self, df, table_name, schema=None, dtype=None, if_exists='replace', index=False, use_fast=True):
        """
        Writes Pandas Dataframe to Table in DB

        Keyword Args:
            user_fast: A parameter whether to use a "faster" write from Pandas to SQL. Usually, this should be set to
                       True. In some cases, there are currently some bugs with writing if columns contain commas.
                       In that case, set to False, and will use the regular Pandas write to SQL (with a monkey-patch)
        """
        if schema:
          self.create_schema(schema=schema)

        if use_fast:
            with self.engine.begin() as conn:
                df_to_sql(db_conn=conn,
                          df=df,
                          table_name=table_name,
                          schema=schema,
                          required_type_map=dtype,
                          if_exists=if_exists,
                          use_index=index,
                          chunksize=None)
        else:   
            with self.engine.begin() as conn:
                df.to_sql(name=table_name,
                          con=conn,
                          schema=schema,
                          dtype=dtype,
                          if_exists=if_exists,
                          index=index,
                          chunksize=10000
                         )
