from pandas import DataFrame, read_sql
from sqlalchemy import create_engine, text

from prbr25_startgg_queries.common.logger import setup_logger

logger = setup_logger(__name__)


class Postgres:
    """
    A class to manage PostgreSQL database operations using SQLAlchemy.

    Args:
        username (str): The username for the PostgreSQL database.
        password (str): The password for the PostgreSQL database.
        endpoint (str): The database server endpoint.
        db (str): The name of the database.
        port (int): The port number for the database connection.

    Methods:
        insert_values_to_table(df: DataFrame, table_name: str):
            Inserts values from a pandas DataFrame into the specified table.
            Data is first uploaded to a temporary table, then merged into the target table.
            Handles conflicts on the 'id' column by ignoring duplicate entries.

        query_db(query: str, table_name: str) -> DataFrame:
            Executes a SQL query on the database and returns the result as a pandas DataFrame.
            Logs the query execution and the number of rows returned.
    """

    def __init__(self, username: str, password: str, endpoint: str, db: str, port: int):
        self.engine = create_engine(
            f"postgresql+psycopg2://{username}:{password}@{endpoint}:{port}/{db}"
        )
        logger.debug("Created sqlalchemy engine")

    def insert_values_to_table(self, df: DataFrame, table_name: str) -> int:
        logger.info(f"Started to upload table data for {table_name}")
        df.to_sql(f"{table_name}_tmp", self.engine, if_exists="replace", index=False)
        logger.debug(f"Starting to merge {table_name}_tmp")
        with self.engine.begin() as conn:
            result = conn.execute(
                text(f"""
                INSERT INTO {table_name}
                SELECT * FROM {table_name}_tmp
                ON CONFLICT (id) DO NOTHING;
            """)
            )
            inserted_rows = result.rowcount
            conn.execute(text(f"DROP TABLE {table_name}_tmp;"))
        logger.info(
            f"Finished uploading data for {table_name}, inserted {inserted_rows} rows"
        )
        return inserted_rows

    def query_db(self, query: str, table_name: str) -> DataFrame:
        logger.info(f"Performing query on {table_name}")
        with self.engine.connect() as conn:
            df = read_sql(text(query), conn)
        logger.debug(f"Query on {table_name} successful, returned {df.shape[0]} rows")
        return df
