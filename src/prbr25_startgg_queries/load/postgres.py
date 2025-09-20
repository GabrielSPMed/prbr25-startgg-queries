from pandas import DataFrame
from sqlalchemy import create_engine, text

from prbr25_startgg_queries.common.logger import setup_logger

logger = setup_logger(__name__)


class Postgres:
    def __init__(self, username: str, password: str, endpoint: str, db: str, port: int):
        self.engine = create_engine(
            f"postgresql+psycopg2://{username}:{password}@{endpoint}:{port}/{db}"
        )
        logger.debug("Created sqlalchemy engine")

    def insert_values_to_table(self, df: DataFrame, table_name: str):
        logger.info("Started to upload table data")
        df.to_sql(f"{table_name}_tmp", self.engine, if_exists="replace", index=False)
        logger.debug("Starting to merge")
        with self.engine.begin() as conn:
            conn.execute(
                text(f"""
                INSERT INTO {table_name}
                SELECT * FROM {table_name}_tmp
                ON CONFLICT (id) DO NOTHING;
            """)
            )
            conn.execute(text(f"DROP TABLE {table_name}_tmp;"))
        logger.info("Finished uploading data")
