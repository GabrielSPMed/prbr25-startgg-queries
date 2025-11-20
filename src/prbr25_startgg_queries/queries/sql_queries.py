most_recent_raw_event_query = """
        SELECT *
        FROM raw_events
        ORDER BY start_at DESC
        LIMIT 1
    """


def get_update_query(table_name: str, column_name: str, ids: str, value) -> str:
    query = f"""
            UPDATE {table_name}
            SET {column_name} = {value}
            WHERE id IN ({ids})
        """
    return query
