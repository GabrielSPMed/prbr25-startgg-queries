from typing import List, Tuple

from pandas import DataFrame, to_datetime

from prbr25_startgg_queries.common.logger import setup_logger
from prbr25_startgg_queries.transform.clean_events import (
    clean_event_and_phases_dataframes,
)
from prbr25_startgg_queries.transform.extract_event_phases import (
    extract_phase_and_event_from_response,
)

logger = setup_logger(__name__)


def transform_tournaments_to_event_phases_df(
    raw_data: List,
) -> Tuple[DataFrame, DataFrame]:
    """
    Transforms raw tournament data into cleaned event and phase DataFrames.

    This function extracts event and phase information from the provided raw data,
    logs the number of unique tournaments found, cleans the resulting DataFrames,
    adds a 'validated' column to the event DataFrame, and converts timestamp columns
    to datetime objects.

    Args:
        raw_data (List): A list containing raw tournament data responses.

    Returns:
        Tuple[DataFrame, DataFrame]: A tuple containing the cleaned event DataFrame
        and phase DataFrame.
    """
    event_df, phase_df = extract_phase_and_event_from_response(raw_data)
    logger.info(
        f"Obtained {len(event_df.tournament_name.unique())} different tournaments"
    )
    event_df, phase_df = clean_event_and_phases_dataframes(event_df, phase_df)
    event_df["validated"] = False
    event_df = convert_timestamp_columns_to_datetime(
        event_df, ["start_at", "last_update_at"]
    )
    return event_df, phase_df


def convert_timestamp_columns_to_datetime(
    df: DataFrame, col_names: List[str]
) -> DataFrame:
    """
    Converts specified timestamp columns in a DataFrame to UTC datetime objects.

    Parameters:
        df (DataFrame): The input pandas DataFrame containing timestamp columns.
        col_names (List[str]): List of column names in `df` to convert from Unix timestamp to datetime.

    Returns:
        DataFrame: The DataFrame with specified columns converted to UTC datetime.
    """
    for col in col_names:
        df[col] = to_datetime(df[col], unit="s", utc=True)
    return df
