most_recent_raw_event_query = """
        SELECT *
        FROM raw_events
        ORDER BY start_at DESC
        LIMIT 1
    """


def get_update_query(table_name: str, column_name: str, ids: str, value) -> str:
    # Format value based on type
    if isinstance(value, bool):
        # PostgreSQL boolean literals
        value_formatted = "TRUE" if value else "FALSE"
    elif isinstance(value, str):
        # Escape single quotes and wrap in quotes
        value_formatted = f"'{value.replace("'", "''")}'"
    elif value is None:
        value_formatted = "NULL"
    else:
        # Numbers and other types
        value_formatted = str(value)

    query = f"""
            UPDATE {table_name}
            SET {column_name} = {value_formatted}
            WHERE id IN ({ids})
        """
    return query
