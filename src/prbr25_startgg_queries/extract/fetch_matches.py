from prbr25_rds_client.postgres import Postgres

from prbr25_startgg_queries.common.config import STARTGG_BEARER_TOKEN
from prbr25_startgg_queries.extract.graphql import GraphQL


def fetch_phase_ids_from_event(sql: Postgres, event_id: int) -> list[int]:
    table = "raw_phases"
    query = f"SELECT id FROM {table} WHERE event_id = {event_id}"
    event_ids_df = sql.query_db(query, table)
    return list(event_ids_df["id"])


def fetch_matches_from_phase_id(phase_id: int, nodes_per_page: int) -> list[dict]:
    return GraphQL(STARTGG_BEARER_TOKEN).query_all_pages_phases(
        "matches",
        {
            "phaseid": f"{phase_id}",
            "perPage": nodes_per_page,
            "cPage": 1,
        },
    )


def fetch_all_matches(phase_id_list: list[int], nodes_per_page: int):
    matches_raw_list = []
    for phase_id in phase_id_list:
        matches_raw_list.extend(fetch_matches_from_phase_id(phase_id, nodes_per_page))
    return matches_raw_list
