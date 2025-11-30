from prbr25_startgg_queries.common.config import STARTGG_BEARER_TOKEN
from prbr25_startgg_queries.extract.graphql import GraphQL


def get_entrants_dict_list(event_id: int, perpage: int) -> list:
    return GraphQL(STARTGG_BEARER_TOKEN).query_all_pages(
        "entrants",
        {
            "eventid": f"{event_id}",
            "perPage": perpage,
            "cPage": 1,
        },
    )
