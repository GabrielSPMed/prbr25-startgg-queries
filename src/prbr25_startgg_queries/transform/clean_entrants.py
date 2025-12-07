from pandas import DataFrame
from prbr25_logger.logger import setup_logger

from prbr25_startgg_queries.common.config import entrant_table_columns

logger = setup_logger(__name__)


def create_dataframe_from_entrants_dict(entrants_dict_list: list) -> DataFrame:
    page_counter = 1
    player_counter = 1
    event_id = entrants_dict_list[0]["event"]["id"]
    logger.info(f"Extracting entrants for event id: {event_id}")
    entrants_df = create_empty_entrant_dataframe(entrant_table_columns)

    for entrant_dict_page in entrants_dict_list:
        logger.debug(f"PAGE {page_counter}:")
        entrants_per_page = entrant_dict_page["event"]["entrants"]["nodes"]
        for entrant in entrants_per_page:
            logger.debug(f"PLAYER {player_counter}:")
            entrants_df = add_entrant_to_entrant_df(entrants_df, entrant, event_id)
            player_counter += 1
        page_counter += 1
    entrants_df["validated"] = False
    return entrants_df


def create_empty_entrant_dataframe(columns: list) -> DataFrame:
    return DataFrame(columns=columns)


def add_entrant_to_entrant_df(
    entrant_df: DataFrame, entrant: dict, event_id: int
) -> DataFrame:
    logger.debug(f"entrant_id: {entrant['id']}")
    logger.debug(f"name: {entrant['name']}")
    try:
        logger.debug(f"slug: {entrant['participants'][0]['user']['slug']}")
        logger.debug(f"player id: {entrant['participants'][0]['user']['player']['id']}")
        logger.debug(
            f"gamertag: {entrant['participants'][0]['user']['player']['gamerTag']}\n"
        )
        entrant_df.loc[len(entrant_df)] = {
            "id": entrant["id"],
            "tag": entrant["participants"][0]["user"]["player"]["gamerTag"],
            "event_id": event_id,
            "url": f"https://start.gg/{entrant['participants'][0]['user']['slug']}",
            "player_id": entrant["participants"][0]["user"]["player"]["id"],
        }
    except Exception:
        logger.debug("ANONYMOUS PLAYER\n")
        entrant_df.loc[len(entrant_df)] = {
            "id": entrant["id"],
            "tag": entrant["name"],
            "event_id": event_id,
        }
    return entrant_df
