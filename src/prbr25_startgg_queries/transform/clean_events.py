from typing import Tuple

import pandas as pd


def get_event_ids_from_tournaments_completed(events: pd.DataFrame) -> pd.Series:
    return events.loc[events.event_state == "COMPLETED", "id"]


def select_series_from_dataframe_column_subset(
    df: pd.DataFrame, column_name: str, series: pd.Series
) -> pd.DataFrame:
    return df.loc[df[column_name].isin(series)].reset_index(drop=True)


def get_phase_ids_from_double_elimination(phases: pd.DataFrame) -> pd.Series:
    return phases.loc[phases.bracket_type == "DOUBLE_ELIMINATION", "event_id"]


def clean_event_and_phases_dataframes(
    events: pd.DataFrame, phases: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
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
