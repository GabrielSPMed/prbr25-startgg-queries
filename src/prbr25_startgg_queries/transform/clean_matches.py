from pandas import DataFrame, concat

from prbr25_startgg_queries.common.config import matches_table_columns


def create_empty_matches_dataframe() -> DataFrame:
    return DataFrame(columns=matches_table_columns)


def create_dataframe_from_raw_matches_list(raw_matches_list: list) -> DataFrame:
    matches_df = create_empty_matches_dataframe()
    for phase in raw_matches_list:
        phase_id = int(phase["phase"]["id"])
        matches_df = create_dataframe_from_matches_in_phase(phase, matches_df, phase_id)
    return matches_df


def create_dataframe_from_matches_in_phase(
    phase: dict, matches_df: DataFrame, phase_id: int
) -> DataFrame:
    for game_set in phase["phase"]["sets"]["nodes"]:
        matches_df = add_row_to_matches_df(game_set, matches_df, phase_id)
    return matches_df


def add_row_to_matches_df(game_set: dict, matches_df: DataFrame, phase_id: int):
    ids = {game_set["slots"][0]["entrant"]["id"], game_set["slots"][1]["entrant"]["id"]}
    winner_id = game_set["winnerId"]
    loser_id = list(ids - {winner_id})[0]
    if game_set["displayScore"] == "DQ":
        score_p1 = 0
        score_p2 = 0
        dq = True
    else:
        score_p1 = (
            game_set["displayScore"]
            .split(game_set["slots"][0]["entrant"]["name"])[-1]
            .strip(" ")[0]
        )
        score_p2 = (
            game_set["displayScore"]
            .split(game_set["slots"][0]["entrant"]["name"])[-1]
            .strip(" ")[-1]
        )
        dq = False
    new_row = DataFrame(
        [
            {
                "player_1_id": int(game_set["slots"][0]["entrant"]["id"]),
                "player_2_id": int(game_set["slots"][1]["entrant"]["id"]),
                "player_1_gamecount": int(score_p1),
                "player_2_gamecount": int(score_p2),
                "winning_player_id": int(winner_id),
                "losing_player_id": int(loser_id),
                "phase_id": phase_id,
                "round": game_set["fullRoundText"],
                "dq": dq,
                "id": game_set["id"],
            }
        ]
    )
    return concat([matches_df, new_row], ignore_index=True)
