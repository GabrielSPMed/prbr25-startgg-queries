from typing import Dict

from prbr25_rds_client.postgres import Postgres


def load_pandas_dataframes_into_postgres(sql: Postgres, dataframes_dict: Dict):
    """
    Loads multiple pandas DataFrames into corresponding PostgreSQL tables.

    Args:
        sql (Postgres): An instance of the Postgres class used to interact with the database.
        dataframes_dict (Dict): A dictionary where keys are table names (str) and values are pandas DataFrames to be inserted.

    Returns:
        None

    Raises:
        Exception: Propagates any exceptions raised during the insertion process.
    """
    for table_name, df in dataframes_dict.items():
        sql.insert_values_to_table(df, table_name)
