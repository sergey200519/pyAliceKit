from typing import Any


DIALOGS_MAP: dict[str, Any] = {
    "/start": {
        "message": "start_message",
        "buttons": ["main_buttons"],
        "events": ["on_start"],
        "meta": {
            "desc": "Точка входа. Предлагает начать историю.",
            "version": "1.0"
        }
    },
    "/stop": {
        "message": "end_message",
        "buttons": ["start_buttons"],
        "events": ["on_stop"],
        "meta": {
            "desc": "Выход из диалога.",
            "version": "1.0"
        }
    },
    "/help": {
        "message": "help",
        "buttons": ["main_buttons"],
        "events": ["on_help"],
        "meta": {
            "desc": "Справка по доступным командам.",
            "version": "1.0"
        }
    },
    "/start_story": {
        "message": "start_story_message",
        "buttons": ["left", "right"],
        "events": ["on_start_story"],
        "childs": ["/start_story/left", "/start_story/right"],
        "transitions": {
            "help": "help",
            "previous": "$prev"
        },
        "meta": {
            "desc": "Начало истории. Выбор направления.",
            "version": "1.0"
        }
    },
    "/start_story/left": {
                "message": "start_left_message",
                "buttons": ["fight", "run"],
                "events": [],
                "childs": ["/start_story/left/end"],
                "transitions": {
                    "help": "help",
                    "previous": "$prev"
                },
                "meta": {
                    "desc": "Левая ветка истории: лес и волк.",
                    "version": "1.0"
                }
            },
    "/start_story/left/end": {
                        "message": "left_end_message",
                        "buttons": [],
                        "events": ["on_end"],
                        "transitions": {
                            "previous": "$prev"
                        },
                        "meta": {
                            "desc": "Конец левой ветки.",
                            "version": "1.0"
                        },
                        "end_dialog": True
                    },
    "/start_story/right": {
                "message": "start_right_message",
                "buttons": ["talk", "hide"],
                "events": [],
                "childs": ["/start_story/right/talk", "/start_story/right/hide"],
                "chooser": """def choose_right_path(user_input: str) -> str:
    lowered = user_input.lower()
    if "поговор" in lowered or "разговор" in lowered:
        return "right_talk"
    elif "спрят" in lowered or "пряч" in lowered:
        return "right_hide"
    return "" """,
                "transitions": {
                    "help": "help",
                    "previous": "$prev"
                },
                "meta": {
                    "desc": "Правая ветка истории: город и человек.",
                    "version": "1.0"
                }
            },
    "/start_story/right/talk": {
                        "message": "right_talk_message",
                        "buttons": [],
                        "events": ["on_end"],
                        "transitions": {
                            "previous": "$prev"
                        },
                        "meta": {
                            "desc": "Диалог с человеком в городе.",
                            "version": "1.0"
                        }
                    },
    "/start_story/right/hide": {
                        "message": "right_hide_message",
                        "buttons": [],
                        "events": ["on_end"],
                        "transitions": {
                            "previous": "$prev"
                        },
                        "meta": {
                            "desc": "Ты спрятался в переулке.",
                            "version": "1.0"
                        }
                    },
}