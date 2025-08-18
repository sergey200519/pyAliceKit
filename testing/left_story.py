from typing import Any

from pyAliceKit.utils.dialogs import include_nodes


left_story: dict[Any, Any] = include_nodes({
    "message": "start_left_message",
    "buttons": ["$fight_or_run"],
    "events": [],
    "keywords": ["left"],
    "childs": {
        "end": {
            "message": "left_end_message",
            "buttons": [],
            "events": ["on_end"],
            "transitions": ["$prev"],
            "meta": {
                "desc": "Конец левой ветки.",
                "version": "1.0"
            },
            "end_dialog": True
        },
    },
    "transitions": ["/help"],
    "meta": {
        "desc": "Левая ветка истории: лес и волк.",
        "version": "1.0"
    }
}, True)
