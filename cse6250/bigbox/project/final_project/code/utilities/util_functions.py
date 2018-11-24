"""Miscellaneous Utility Functions"""
import csv
import git
import logging
import tempfile

LOGGER = logging.getLogger(__name__)


def get_git_root(path):
    """Return Top Level Git Repository directory given path"""
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


def df_to_sql(db_conn, df, table_name, schema, required_type_map=None,
              use_index=False,
              sep='|',
              encoding='utf8',
              temp_file_func=tempfile.SpooledTemporaryFile,
              if_exists='replace',
              chunksize=None):
    """Helper for writing a pandas.Dataframe to SQL
    Args:
        db_conn (sqlalchemy.engine.Connection):
        df (pandas.DataFrame): the dataframe to write to sql
        table_name (str): the output table name
        schema (str): the output schema name
        required_type_map (dict): optional mapping of column names to sqlalchemy types
        use_index (boolean):
        sep (str): separator for temp file
        encoding (str): encoding for temp file
        temp_file_func (tempfile.TemporaryFile): function to call for building
            temp file. Passed as default arg so this works in tests when mocking
            out the filesystem
        if_exists (str): what to do if table exists. 'append' and 'replace' are supported
    Has been benchmarked to be faster than pd.to_sql, odo, and other pandas hacks
    """
    assert if_exists in ['append', 'replace']
    if required_type_map and \
            any(col not in df.columns for col in required_type_map.keys()):  # pragma: no cover
        raise TypeError('required_type_map contains invalid columns.')

    # Use DF to create empty table
    LOGGER.info('Replacing %s', table_name)
    df[:0].to_sql(table_name, db_conn,
                  if_exists=if_exists,
                  index=use_index,
                  schema=schema,
                  dtype=required_type_map or {})

    with temp_file_func(mode='w+', suffix='.csv') as tmp_file:
        df.to_csv(tmp_file, sep=sep, header=False, quoting=csv.QUOTE_NONE, quotechar='',
                  escapechar='\\', encoding=encoding, index=use_index)
        tmp_file.seek(0)

        with db_conn.connection.cursor() as cursor:
            cursor.copy_from(tmp_file, '.'.join([schema, table_name]), sep=sep, null='')
            LOGGER.info('Completed copy from for %s', table_name)
