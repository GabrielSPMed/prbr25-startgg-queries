def comma_separate_string_list(ls: list) -> str:
    return ", ".join(str(id) for id in ls)
