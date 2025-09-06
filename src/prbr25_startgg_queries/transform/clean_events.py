from typing import Tuple

import pandas as pd


def get_event_ids_from_tournaments_completed(events: pd.DataFrame) -> pd.Series:
    """
    Extracts the IDs of events that have a state marked as "COMPLETED" from the given DataFrame.

    Args:
        events (pd.DataFrame): A DataFrame containing event data with at least 'event_state' and 'id' columns.

    Returns:
        pd.Series: A Series containing the IDs of events where 'event_state' is "COMPLETED".
    """
    return events.loc[events.event_state == "COMPLETED", "id"]


def select_series_from_dataframe_column_subset(
    df: pd.DataFrame, column_name: str, series: pd.Series
) -> pd.DataFrame:
    """
    Filters a DataFrame by selecting rows where the values in a specified column are present in a given Series.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column_name (str): The name of the column to check for membership.
        series (pd.Series): The Series containing values to match in the column.

    Returns:
        pd.DataFrame: A new DataFrame containing only the rows where the column's value is in the Series, with the index reset.
    """
    return df.loc[df[column_name].isin(series)].reset_index(drop=True)


def get_phase_ids_from_double_elimination(phases: pd.DataFrame) -> pd.Series:
    """
    Extracts the event IDs from phases with a 'DOUBLE_ELIMINATION' bracket type.

    Args:
        phases (pd.DataFrame): DataFrame containing phase information, including 'bracket_type' and 'event_id' columns.

    Returns:
        pd.Series: Series of event IDs corresponding to phases with a 'DOUBLE_ELIMINATION' bracket type.
    """
    return phases.loc[phases.bracket_type == "DOUBLE_ELIMINATION", "event_id"]


def clean_event_and_phases_dataframes(
    events: pd.DataFrame, phases: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cleans and filters the provided events and phases DataFrames by applying the following steps:
    1. Selects events that are marked as completed.
    2. Filters phases to include only those associated with completed events.
    3. Identifies phases that use double elimination format.
    4. Further filters events and phases to include only those associated with double elimination phases.

    Args:
        events (pd.DataFrame): DataFrame containing event data.
        phases (pd.DataFrame): DataFrame containing phase data.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the filtered events and phases DataFrames.
    """
    completed_events = get_event_ids_from_tournaments_completed(events)
    events = select_series_from_dataframe_column_subset(events, "id", completed_events)
    phases = select_series_from_dataframe_column_subset(
        phases, "event_id", completed_events
    )
    double_elimination_phases = get_phase_ids_from_double_elimination(phases)
    events = select_series_from_dataframe_column_subset(
        events, "id", double_elimination_phases
    )
    phases = select_series_from_dataframe_column_subset(
        phases, "event_id", double_elimination_phases
    )
    return events, phases
