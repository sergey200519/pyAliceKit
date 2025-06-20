def from_str_bool_to_py_bool(boolean: str | bool) -> bool | int:
    if type(boolean) is str:
        if boolean == "true":
            return True
        elif boolean == "false":
            return False
    elif type(boolean) is bool:
        return boolean
    return -1