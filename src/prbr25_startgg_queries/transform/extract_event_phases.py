from typing import Dict, List, Tuple


def extract_phase_and_event_from_response(response: List) -> Tuple[List, List]:
    """
    Extracts events and phases from a list of tournament responses.

    Iterates over each tournament in the response, extracting events and phases using
    the `extract_events_and_phases_from_tournament` function, and aggregates them into separate lists.

    Args:
        response (List): A list of tournament response objects.

    Returns:
        Tuple[List, List]: A tuple containing two lists:
            - The first list contains all extracted events.
            - The second list contains all extracted phases.
    """
    event_list = []
    phase_list = []
    for tournament in response:
        event_list.extend(extract_events_and_phases_from_tournament(tournament)[0])
        phase_list.extend(extract_events_and_phases_from_tournament(tournament)[1])
    return event_list, phase_list


def extract_events_and_phases_from_tournament(tournament: Dict) -> Tuple[List, List]:
    """
    Extracts event and phase information from a tournament dictionary.

    Iterates through all events in the provided tournament, generating a list of event dictionaries
    and a list of phase dictionaries by calling helper functions for each event.

    Args:
        tournament (Dict): A dictionary containing tournament data, including an "events" key.

    Returns:
        Tuple[List, List]: A tuple containing:
            - A list of event dictionaries.
            - A list of phase dictionaries extracted from all events.
    """
    event_list = []
    phase_list = []
    for event in tournament["events"]:
        event_list.append(fill_event_dict(event, tournament))
        phase_list.extend(extract_phases_from_event(event))
    return event_list, phase_list


def extract_phases_from_event(event: Dict) -> List:
    """
    Extracts phase information from an event dictionary.

    Iterates over the "phases" in the given event and constructs a list of phase dictionaries
    using the `fill_phase_dict` function, passing each phase and the event's ID.

    Args:
        event (Dict): A dictionary representing an event, expected to contain an "id" and a "phases" list.

    Returns:
        List: A list of dictionaries, each representing a phase extracted from the event.
    """
    phase_list = []
    for phase in event["phases"]:
        phase_list.append(fill_phase_dict(phase, event["id"]))
    return phase_list


def fill_phase_dict(phase: Dict, event_id: str) -> Dict:
    """
    Populate a dictionary with phase information and associated event ID.

    Args:
        phase (Dict): A dictionary containing phase data with keys "id", "name", and "bracketType".
        event_id (str): The identifier of the event to associate with the phase.

    Returns:
        Dict: A dictionary with keys "id", "name", "bracket_type", and "event_id" containing the corresponding values.
    """
    phase_dict = {}
    phase_dict["id"] = phase["id"]
    phase_dict["name"] = phase["name"]
    phase_dict["bracket_type"] = phase["bracketType"]
    phase_dict["event_id"] = event_id
    return phase_dict


def fill_event_dict(event: Dict, tournament: Dict) -> Dict:
    """
    Populate a dictionary with event and tournament details.

    Args:
        event (Dict): A dictionary containing event information.
        tournament (Dict): A dictionary containing tournament information.

    Returns:
        Dict: A dictionary with combined event and tournament details, including tournament ID, name, location, URL, event ID, state, name, number of entrants, start time, and last update time.
    """
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
