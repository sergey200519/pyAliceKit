import inspect
import os
import json
from typing import Any, Union


def include_nodes(obj: dict[str, Any], DEBUG: bool) -> dict[str, Any]:
    if not DEBUG:
        return obj

    frame_info = inspect.stack()[1]
    frame = frame_info.frame
    filename = frame.f_globals.get("__file__", None)

    import_name = None
    for name, val in frame.f_globals.items():
        if val is obj:
            import_name = name
            break

    # Определяем уровень вложенности
    def get_depth(o: Any, level=1) -> int:
        if isinstance(o, dict):
            for v in o.values():
                if isinstance(v, dict) and "__source__" in v:
                    return get_depth(v["__value__"], level + 1)
        return level

    depth = get_depth(obj)

    return {
        "__value__": obj,
        "__source__": {
            "parent": filename,
            "depth": depth,
            "dependencies": {
                filename: {
                    "import_name": import_name,
                    "value": obj,
                    "depth": depth
                }
            }
        }
    }



test3 = {
    "sec": "test3"
}

insertion = {
    "key-i": "value",
    "secp": include_nodes(test3, True)
}

