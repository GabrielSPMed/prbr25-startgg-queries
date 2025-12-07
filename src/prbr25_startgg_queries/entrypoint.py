from prbr25_logger.logger import setup_logger
from prbr25_rds_client.postgres import Postgres

from prbr25_startgg_queries.common.config import (
    EVENTS_PER_PAGE,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USERNAME,
)
from prbr25_startgg_queries.common.list_utils import comma_separate_string_list
from prbr25_startgg_queries.extract.load_entrants_from_event import (
    get_entrants_dict_list,
)
from prbr25_startgg_queries.extract.refresh_raw import (
    extract_event_and_phase_dfs_from_timestamp,
)
from prbr25_startgg_queries.extract.tournament_from_url import (
    request_tournament_from_url,
)
from prbr25_startgg_queries.load.utils import load_pandas_dataframes_into_postgres
from prbr25_startgg_queries.queries.sql_queries import get_update_query
from prbr25_startgg_queries.transform.clean_entrants import (
    create_dataframe_from_entrants_dict,
)
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


def edit_filtered_column_from_id(ids: list, table_name: str, column_name: str, value):
    sql = Postgres(
        POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB, POSTGRES_PORT
    )
    id_cs = comma_separate_string_list(ids)
    query = get_update_query(table_name, column_name, id_cs, value)
    sql.execute_update(query)


def update_entrants_table_from_event_id(event_id: int):
    sql = Postgres(
        POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB, POSTGRES_PORT
    )
    entrants_dict_list = get_entrants_dict_list(event_id, EVENTS_PER_PAGE)
    entrants_df = create_dataframe_from_entrants_dict(entrants_dict_list)
    sql.insert_values_to_table(entrants_df, "entrants")
