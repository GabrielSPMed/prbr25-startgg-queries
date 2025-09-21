from os import environ

from dotenv import load_dotenv

load_dotenv()

STARTGG_BEARER_TOKEN = environ["STARTGG_BEARER_TOKEN"]
POSTGRES_USERNAME = environ["POSTGRES_USERNAME"]
POSTGRES_PASSWORD = environ["POSTGRES_PASSWORD"]
POSTGRES_PORT = int(environ["POSTGRES_PORT"])
POSTGRES_DB = environ["POSTGRES_DB"]
POSTGRES_HOST = environ["POSTGRES_HOST"]
MAX_DATE_LIMIT = int(environ["MAX_DATE_LIMIT"])
MIN_DATE_LIMIT = int(environ["MIN_DATE_LIMIT"])
COUNTRY_CODE = environ["COUNTRY_CODE"]
STARTGG_VIDEOGAME_ID = int(environ["STARTGG_VIDEOGAME_ID"])

events_dict = {
    "cCode": COUNTRY_CODE,
    "perPage": 50,
    "cPage": 1,
    "videogameid": STARTGG_VIDEOGAME_ID,
    "online": False,
    "afterdate": MIN_DATE_LIMIT,
    "beforedate": MAX_DATE_LIMIT,
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
