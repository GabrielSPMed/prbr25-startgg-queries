most_recent_raw_event_query = """
        SELECT *
        FROM raw_events
        ORDER BY start_at DESC
        LIMIT 1
    """
