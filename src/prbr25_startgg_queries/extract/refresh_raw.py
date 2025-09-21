from datetime import datetime, timedelta
from typing import Tuple

from prbr25_startgg_queries.bd.postgres import Postgres
from prbr25_startgg_queries.common.config import MAX_DATE_LIMIT
from prbr25_startgg_queries.common.logger import setup_logger
from prbr25_startgg_queries.queries.sql_queries import most_recent_raw_event_query

logger = setup_logger(__name__)


def get_timestamps_for_refresh(sql: Postgres) -> Tuple[int, int]:
    """
    Calculates the start and end timestamps for refreshing event data.

    The function determines the end timestamp as the current time (capped by MAX_DATE_LIMIT)
    and the start timestamp as two weeks before the most recent raw event in the database.

    Args:
        sql (Postgres): A Postgres database connection or query interface used to fetch the most recent raw event.

    Returns:
        tuple: A tuple containing the start timestamp (int) and end timestamp (int).

    Logs:
        Information about the date range being fetched.
    """
    end_date = datetime.now()
    end_timestamp = min(int(end_date.timestamp()), MAX_DATE_LIMIT)
    start_date = fetch_most_recent_raw_event(sql) - timedelta(weeks=2)
    start_timestamp = int(start_date.timestamp())
    logger.info(f"Will fetch events that started between {start_date} and {end_date}")
    return start_timestamp, end_timestamp


def fetch_most_recent_raw_event(sql: Postgres):
    """
    Fetches the most recent raw event from the database.

    Executes a query to retrieve the latest event from the "raw_events" table,
    logs the tournament and event details, and returns the start date of the event.

    Args:
        sql (Postgres): An instance of the Postgres database connection.

    Returns:
        Any: The start date of the most recent event.
    """
    most_recent_event = sql.query_db(
        most_recent_raw_event_query, "raw_events"
    ).to_dict()
    logger.info(
        f"The most recent tournament in the database is: {most_recent_event['tournament_name'][0]}: {most_recent_event['event_name'][0]} at {most_recent_event['start_at'][0]}"
    )
    return most_recent_event["start_at"][0]
