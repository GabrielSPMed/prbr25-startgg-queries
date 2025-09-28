from typing import List

from prbr25_startgg_queries.common.config import (
    STARTGG_BEARER_TOKEN,
    STARTGG_VIDEOGAME_ID,
)
from prbr25_startgg_queries.common.logger import setup_logger
from prbr25_startgg_queries.extract.graphql import GraphQL

logger = setup_logger(__name__)


def request_tournament_from_url(url: str) -> List:
    """
    Fetches tournament data from a given StartGG URL.

    Args:
        url (str): The URL of the StartGG tournament.

    Returns:
        dict: Raw tournament data retrieved from the GraphQL API.

    Raises:
        ValueError: If the URL is invalid or the tournament cannot be found.
        Exception: For any other errors during the GraphQL query.
    """
    slug = get_slug_from_url(url)
    logger.debug(f"Slug queried: {slug}")
    tournament_dict = {"tournamentslug": slug, "videogameid": STARTGG_VIDEOGAME_ID}
    raw_tournament_data = GraphQL(STARTGG_BEARER_TOKEN).query_tournament(
        "find_tournament", tournament_dict
    )
    return raw_tournament_data


def get_slug_from_url(url: str):
    """
    Extracts the tournament slug from a StartGG tournament URL.

    Args:
        url (str): The URL of the StartGG tournament.

    Returns:
        str: The tournament slug extracted from the URL.

    Raises:
        IndexError: If the URL does not contain 'tournament/' or the expected format.
    """
    return url.split("tournament/")[1].split("/")[0]
