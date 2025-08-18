from typing import Any

from pyAliceKit.py_alice.py_alice import PyAlice
from pyAliceKit.utils.dialogs import include_nodes


def choose_right_path(pyAlice: "PyAlice") -> str:
    print("choose_right_path called with user_input:", pyAlice)
    if "поговорить" in pyAlice.came_message or "разговор" in pyAlice.came_message:
        return "/start_story/right/talk"
    elif "спрятаться" in pyAlice.came_message or "прятаться" in pyAlice.came_message:
        return "/start_story/right/hide"
    return "/start_story/right/talk"


right_story: dict[Any, Any] = include_nodes({
    "message": "start_right_message",
    "buttons": ["$right"],
    "events": [],
    "keywords": ["right"],
    "childs": {
        "talk": {
            "message": "right_talk_message",
            "buttons": [],
            "events": ["on_end"],
            "transitions": ["$prev"],
            "meta": {
                "desc": "Диалог с человеком в городе.",
                "version": "1.0"
            }
        },

        "hide": {
            "message": "right_hide_message",
            "buttons": [],
            "events": ["on_end"],
            "transitions": ["$prev"],
            "meta": {
                "desc": "Ты спрятался в переулке.",
                "version": "1.0"
            }
        },
    },
    "chooser": choose_right_path,
    "transitions": ["/help", "$prev"],
    "meta": {
        "desc": "Правая ветка истории: город и человек.",
        "version": "1.0"
    }
}, True)