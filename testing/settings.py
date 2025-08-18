from typing import Any

from testing.images import images
from testing.left_story import left_story
from testing.right_story import right_story
from testing.all_messages import messages


EVENTS = True
DEBUG = True
LOG_OUTPUT_IMMEDIATELY = True
TIME_ZONE = None


TEXT_FOR_KEY_WORDS = "command"
VERSION = "1.0"


DIALOG_NODES: dict[str, Any] = {
    "stop": {
        "message": "end_message",
        "buttons": ["$start_buttons"],
        "events": ["on_stop"],
        "meta": {
            "desc": "Выход из диалога.",
            "version": "1.0"
        }
    },

    "help": {
        "message": "help",
        "buttons": ["$main_buttons"],
        "events": ["on_help"],
        "keywords": ["help"],
        "meta": {
            "desc": "Справка по доступным командам.",
            "version": "1.0"
        }
    },

    "start_story": {
        "message": "start_story_message",
        "buttons": ["$left"],
        "events": ["on_start_story"],
        "keywords": ["start"],
        "image": "img1",
        "childs": {
            "left": left_story,
            "right": right_story
        },
        "transitions": ["/help", "$prev"],
        "meta": {
            "desc": "Начало истории. Выбор направления.",
            "version": "1.0"
        }
    },  
}

DIALOG_NODES_WITH_META = "" #нужно както реализовать, возможно нужно реализовать новую фуенкцию

DIALOGS_MAP_FILE = "testing/dialogs_map.json"


ALL_MESSAGES = messages

STARTING_MESSAGE = "start_message"
ERROR_MESSAGE = "help"
HELP_MESSAGE = "help"
MORE_DATA_MESSAGES = {}


BUTTONS: dict[str, Any] = {
    "start_btn": {
        "title": "Начать",
        "hide": False
    },
    "stop_btn": {
        "title": "Стоп",
        "hide": False
    },
    "help_btn": {
        "title": "Помощь",
        "hide": False
    },
    "left_btn": {
        "title": "Пойти налево",
        "hide": False
    },
    "right_btn": {
        "title": "Пойти направо",
        "hide": False
    },
    "fight_btn": {
        "title": "Сразиться",
        "hide": False
    },
    "run_btn": {
        "title": "Убежать",
        "hide": False
    },
    "talk_btn": {
        "title": "Поговорить",
        "hide": False
    },
    "hide_btn": {
        "title": "Спрятаться",
        "hide": False
    }
}
# TODO: Add messages and valifdate
CONSTANT_BUTTONS = ["$const_btn", "help_btn"]
BUTTONS_GROUPS = {
    "$const_btn": ["start_btn", "stop_btn"],
    "$main_buttons": ["start_btn", "stop_btn", "help_btn"],
    "$start_buttons": ["start_btn"],
    "$left": ["left_btn", "right_btn"],
    "$right": ["talk_btn", "hide_btn"],
    "$fight_or_run": ["fight_btn", "run_btn"],
}
STARTING_BUTTONS = []

KEY_WORDS = {
    "start": ["начать", "старт", "запустить", "привет"],
    "stop": ["стоп", "остановить", "выключить", "закрыть"],
    "help": ["помощь", "справка", "подсказка"],
    "prev": ["назад", "предыдущий", "вернуться"],
    "next": ["далее", "следующий", "продолжить"],
    "left": ["налево", "влево", "лес"],
    "right": ["направо", "вправо", "город"],
    "hide": ["спрятаться", "скрыться", "прятаться"],
    "talk": ["поговорить", "разговор", "общаться"],
}

IMAGES = images

DEBUG_LANGUAGE = "ru"
LANGUAGE = "ru"
SOURCE_TEXT = "command"
