from typing import Dict, List, Tuple

phase_table_columns = ["id", "name", "bracket_type", "event_id"]


def extract_phase_and_event_from_response(response: List) -> Tuple[List, List]:
    event_list = []
    phase_list = []
    for tournament in response:
        event_list.extend(extract_events_and_phases_from_tournament(tournament)[0])
        phase_list.extend(extract_events_and_phases_from_tournament(tournament)[1])
    return event_list, phase_list


def extract_events_and_phases_from_tournament(tournament: Dict) -> Tuple[List, List]:
    event_list = []
    phase_list = []
    for event in tournament["events"]:
        event_list.append(fill_event_dict(event, tournament))
        phase_list.extend(extract_phases_from_event(event))
    return event_list, phase_list


def extract_phases_from_event(event: Dict) -> List:
    phase_list = []
    for phase in event["phases"]:
        phase_list.append(fill_phase_dict(phase, event["id"]))
    return phase_list


def fill_phase_dict(phase: Dict, event_id: str) -> Dict:
    phase_dict = {}
    phase_dict["id"] = phase["id"]
    phase_dict["name"] = phase["name"]
    phase_dict["bracket_type"] = phase["bracketType"]
    phase_dict["event_id"] = event_id
    return phase_dict


def fill_event_dict(event: Dict, tournament: Dict) -> Dict:
    event_dict = {}
    event_dict["tournament_id"] = tournament["id"]
    event_dict["tournament_name"] = tournament["name"]
    event_dict["address_state"] = tournament["addrState"]
    event_dict["city"] = tournament["city"]
    event_dict["url"] = tournament["url"]
    event_dict["id"] = event["id"]
    event_dict["event_state"] = event["state"]
    event_dict["event_name"] = event["name"]
    event_dict["num_entrants"] = event["numEntrants"]
    event_dict["start_at"] = event["startAt"]
    event_dict["last_update_at"] = event["updatedAt"]
    return event_dict
