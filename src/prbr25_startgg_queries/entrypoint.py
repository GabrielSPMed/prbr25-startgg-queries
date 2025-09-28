from prbr25_startgg_queries.bd.postgres import Postgres
from prbr25_startgg_queries.common.config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USERNAME,
)
from prbr25_startgg_queries.common.logger import setup_logger
from prbr25_startgg_queries.extract.refresh_raw import (
    extract_event_and_phase_dfs_from_timestamp,
)
from prbr25_startgg_queries.extract.tournament_from_url import (
    request_tournament_from_url,
)
from prbr25_startgg_queries.load.utils import load_pandas_dataframes_into_postgres
from prbr25_startgg_queries.transform.utils import (
    transform_tournaments_to_event_phases_df,
)

logger = setup_logger(__name__)


def refresh_raw_events():
    """
    Extracts event and phase data from a PostgreSQL database, transforms the data into pandas DataFrames,
    and loads the resulting DataFrames back into the database as 'raw_events' and 'raw_phases' tables.

    Steps:
        1. Connects to the PostgreSQL database using provided credentials.
        2. Extracts raw event and phase data based on timestamps.
        3. Transforms the extracted data into event and phase DataFrames.
        4. Loads the DataFrames into the database.

    Raises:
        Exception: If any step in the extraction, transformation, or loading process fails.
    """
    sql = Postgres(
        POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB, POSTGRES_PORT
    )
    raw_data = extract_event_and_phase_dfs_from_timestamp(sql)
    event_df, phase_df = transform_tournaments_to_event_phases_df(raw_data)
    load_pandas_dataframes_into_postgres(
        sql, {"raw_events": event_df, "raw_phases": phase_df}
    )


def retrieve_events_and_phases_from_tournament_url(url: str):
    """
    Retrieves event and phase data from a tournament URL, transforms the data into pandas DataFrames,
    and loads them into a PostgreSQL database.

    Args:
        url (str): The URL of the tournament to retrieve data from.

    Returns:
        None
    """
    sql = Postgres(
        POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB, POSTGRES_PORT
    )
    raw_data = request_tournament_from_url(url)
    event_df, phase_df = transform_tournaments_to_event_phases_df(raw_data)
    load_pandas_dataframes_into_postgres(
        sql, {"raw_events": event_df, "raw_phases": phase_df}
    )
