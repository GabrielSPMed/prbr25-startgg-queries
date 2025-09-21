from prbr25_startgg_queries.common.config import STARTGG_BEARER_TOKEN, events_dict
from prbr25_startgg_queries.common.logger import setup_logger
from prbr25_startgg_queries.extract.graphql import GraphQL

logger = setup_logger(__name__)


def request_events(start_date: int, end_date: int):
    """
    Fetches tournament event data within a specified date range.

    Args:
        start_date (int): The start date (timestamp or date integer) to filter events after.
        end_date (int): The end date (timestamp or date integer) to filter events before.

    Returns:
        Any: Raw tournament event data retrieved from the GraphQL API.

    Raises:
        Exception: If the GraphQL query fails or returns an error.
    """
    events_dict["afterdate"] = start_date
    events_dict["beforedate"] = end_date
    raw_tournament_data = GraphQL(STARTGG_BEARER_TOKEN).query_all_pages(
        "events", events_dict
    )
    return raw_tournament_data
