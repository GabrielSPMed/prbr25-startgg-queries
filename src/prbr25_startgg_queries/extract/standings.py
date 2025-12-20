from prbr25_startgg_queries.common.config import STARTGG_BEARER_TOKEN
from prbr25_startgg_queries.extract.graphql import GraphQL


def fetch_standings_from_event_id(event_id: int, nodes_per_page: int) -> list[dict]:
    return GraphQL(STARTGG_BEARER_TOKEN).query_all_pages_standings(
        "standings",
        {
            "eventid": f"{event_id}",
            "perPage": nodes_per_page,
            "cPage": 1,
        },
    )
