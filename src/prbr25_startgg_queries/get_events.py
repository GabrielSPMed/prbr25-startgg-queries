from datetime import datetime

from prbr25_startgg_queries.common.config import STARTGG_BEARER_TOKEN, events_dict
from prbr25_startgg_queries.common.logger import setup_logger
from prbr25_startgg_queries.extract.graphql import GraphQL

logger = setup_logger(__name__)


def request_events(start_date: int, end_date: int):
    events_dict["afterdate"] = start_date
    events_dict["beforedate"] = end_date
    raw_tournament_data = GraphQL(STARTGG_BEARER_TOKEN).query_all_pages(
        "events", events_dict
    )
    print(raw_tournament_data)


end_date = datetime.now()
start_date = datetime(end_date.year, 1, 1)
# start_date = end_date - timedelta(weeks=1)
request_events(int(start_date.timestamp()), int(end_date.timestamp()))
