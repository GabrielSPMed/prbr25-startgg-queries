import pandas as pd

from prbr25_startgg_queries.common.config import STARTGG_BEARER_TOKEN, events_dict
from prbr25_startgg_queries.common.logger import setup_logger
from prbr25_startgg_queries.extract.graphql import GraphQL
from prbr25_startgg_queries.transform.clean_events import (
    clean_event_and_phases_dataframes,
)
from prbr25_startgg_queries.transform.extract_event_phases import (
    extract_phase_and_event_from_response,
)

logger = setup_logger(__name__)


def request_events(start_date: int, end_date: int):
    events_dict["afterdate"] = start_date
    events_dict["beforedate"] = end_date
    raw_tournament_data = GraphQL(STARTGG_BEARER_TOKEN).query_all_pages(
        "events", events_dict
    )
    return raw_tournament_data


def get_events_and_phases(start_timestamp: int, end_timestamp: int):
    data = request_events(start_timestamp, end_timestamp)
    event_list, phase_list = extract_phase_and_event_from_response(data)
    event_df = pd.DataFrame(event_list)
    phase_df = pd.DataFrame(phase_list)
    return clean_event_and_phases_dataframes(event_df, phase_df)


# end_date = datetime.now()
# # start_date = end_date - timedelta(weeks=4)
# start_date = datetime(end_date.year, 1, 1)
# start_timestamp = int(start_date.timestamp())
# end_timestamp = int(end_date.timestamp())
# event_df, phase_df = get_events_and_phases(start_timestamp, end_timestamp)
# event_df.to_csv("test_events.csv")
# phase_df.to_csv("test_phases.csv")
