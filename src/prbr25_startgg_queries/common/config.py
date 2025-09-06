from os import environ

from dotenv import load_dotenv

load_dotenv()

STARTGG_BEARER_TOKEN = environ["STARTGG_BEARER_TOKEN"]

events_dict = {
    "cCode": "BR",
    "perPage": 50,
    "cPage": 1,
    "videogameid": 1386,
    "online": False,
    "afterdate": 1735700400,
    "beforedate": 1755494257,
}

event_table_columns = [
    "tournament_id",
    "tournament_name",
    "address_state",
    "city",
    "url",
    "id",
    "event_state",
    "event_name",
    "num_entrants",
    "start_at",
    "last_update_at	event_value",
]

phase_table_columns = ["id", "name", "bracket_type", "event_id"]
