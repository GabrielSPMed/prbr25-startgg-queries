from pandas import DataFrame, concat

from prbr25_startgg_queries.common.config import standings_table_columns


def create_standings_dataframe_from_response(raw_standings: list) -> DataFrame:
    standings_df = DataFrame(columns=standings_table_columns)
    for standings_chunk in raw_standings:
        standings_df = add_standings_from_chunk(standings_chunk, standings_df)
    return standings_df


def add_standings_from_chunk(
    standings_chunk: dict, standings_df: DataFrame
) -> DataFrame:
    event_id = standings_chunk["event"]["id"]
    for entrant in standings_chunk["event"]["standings"]["nodes"]:
        standings_df = append_standings_row(event_id, entrant, standings_df)
    return standings_df


def append_standings_row(
    event_id: int, entrant: dict, standings_df: DataFrame
) -> DataFrame:
    new_df = DataFrame(
        [
            {
                "id": entrant["id"],
                "event_id": event_id,
                "standing": entrant["placement"],
                "player_id": entrant["entrant"]["id"],
                "dq": False,
                "perf_score": 0,
            }
        ]
    )
    return concat([standings_df, new_df], ignore_index=True)
