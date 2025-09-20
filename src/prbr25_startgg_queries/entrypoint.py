from datetime import datetime

import pandas as pd

from prbr25_startgg_queries.common.config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USERNAME,
)
from prbr25_startgg_queries.common.logger import setup_logger
from prbr25_startgg_queries.extract.utils import request_events
from prbr25_startgg_queries.load.postgres import Postgres
from prbr25_startgg_queries.transform.clean_events import (
    clean_event_and_phases_dataframes,
)
from prbr25_startgg_queries.transform.extract_event_phases import (
    extract_phase_and_event_from_response,
)

logger = setup_logger(__name__)


def refresh_raw_events(start_timestamp: int, end_timestamp: int):
    data = request_events(start_timestamp, end_timestamp)
    event_list, phase_list = extract_phase_and_event_from_response(data)
    event_df = pd.DataFrame(event_list)
    phase_df = pd.DataFrame(phase_list)
    event_df, phase_df = clean_event_and_phases_dataframes(event_df, phase_df)
    event_df["validated"] = False
    event_df["start_at"] = pd.to_datetime(event_df["start_at"], unit="s", utc=True)
    event_df["last_update_at"] = pd.to_datetime(
        event_df["last_update_at"], unit="s", utc=True
    )
    sql = Postgres(
        POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB, POSTGRES_PORT
    )
    sql.insert_values_to_table(event_df, "raw_events")
    sql.insert_values_to_table(phase_df, "raw_phases")


# def main():
#     if len(sys.argv) != 3:
#         print("Usage: <start_timestamp> <end_timestamp>", file=sys.stderr)
#         sys.exit(1)

#     start_ts, end_ts = map(int, sys.argv[1:3])
#     get_events_and_phases(start_ts, end_ts)


# if __name__ == "__main__":
#     main()


end_date = datetime.now()
# start_date = end_date - timedelta(weeks=4)
start_timestamp = 1733022000
end_timestamp = int(end_date.timestamp())
refresh_raw_events(start_timestamp, end_timestamp)
