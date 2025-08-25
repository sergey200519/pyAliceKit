from typing import Any

from testing.river_story import river_story
from testing.forest_story import forest_story
from testing.city_story import city_story
from testing.images import images
from testing.all_messages import messages


EVENTS = True
DEBUG = True
LOG_OUTPUT_IMMEDIATELY = True
TIME_ZONE = None


TEXT_FOR_KEY_WORDS = "command"
VERSION = "1.0"


DIALOG_NODES: dict[str, Any] = {
    "start": {
        "message": "intro_message",
        "buttons": ["$main_start"],
        "events": ["on_start"],
        "keywords": ["start"],
        "meta": {
            "desc": "Начало большого приключения.",
            "version": "2.0"
        },
        "childs": {
            "choose_path": {
                "message": "choose_path_message",
                "buttons": ["$path_choices"],
                "keywords": ["left", "right", "river"],
                "childs": {
                    "forest": forest_story,
                    "city": city_story,
                    "river": river_story
                },
                "transitions": ["/help", "$prev"],
                "meta": {
                    "desc": "Выбор пути: лес, город или река.",
                    "version": "2.0"
                }
            }
        }
    },
    "help": {
        "message": "help",
        "buttons": ["$main_buttons"],
        "events": ["on_help"],
        "keywords": ["help"],
        "meta": {
            "desc": "Справка по доступным командам.",
            "version": "2.0"
        }
    },
    "stop": {
        "message": "end_message",
        "buttons": ["$start_buttons"],
        "events": ["on_stop"],
        "meta": {
            "desc": "Выход из игры.",
            "version": "2.0"
        }
    }
}

DIALOG_NODES_WITH_META = "" #нужно както реализовать, возможно нужно реализовать новую фуенкцию

DIALOGS_MAP_FILE = "testing/dialogs_map.json"


ALL_MESSAGES = messages

STARTING_MESSAGE = "intro_message"
ERROR_MESSAGE = "help"
HELP_MESSAGE = "help"
MORE_DATA_MESSAGES = {}


BUTTONS = {
    "start_btn": {"title": "Начать", "hide": False},
    "stop_btn": {"title": "Стоп", "hide": False},
    "help_btn": {"title": "Помощь", "hide": False},
    "forest_btn": {"title": "Лес", "hide": False},
    "city_btn": {"title": "Город", "hide": False},
    "river_btn": {"title": "Река", "hide": False},
    "fight_btn": {"title": "Сразиться", "hide": False},
    "talk_btn": {"title": "Поговорить", "hide": False},
    "enter_hut_btn": {"title": "Зайти в хижину", "hide": False},
    "continue_btn": {"title": "Идти дальше", "hide": False},
    "merchant_btn": {"title": "К торговцу", "hide": False},
    "inn_btn": {"title": "В трактир", "hide": False},
    "buy_btn": {"title": "Купить меч", "hide": False},
    "skip_btn": {"title": "Отказаться", "hide": False},
    "wine_btn": {"title": "Выпить вина", "hide": False},
    "news_btn": {"title": "Спросить новости", "hide": False},
    "boat_btn": {"title": "Сесть в лодку", "hide": False},
    "bridge_btn": {"title": "Перейти мост", "hide": False},
    "enter_btn": {"title": "Зайти", "hide": False},
}

# TODO: Add messages and valifdate
CONSTANT_BUTTONS = ["help_btn"]
BUTTONS_GROUPS = {
    "$main_start": ["start_btn"],
    "$main_buttons": ["start_btn", "stop_btn", "help_btn"],
    "$start_buttons": ["start_btn"],
    "$path_choices": ["forest_btn", "city_btn", "river_btn"],
    "$forest_choices": ["fight_btn", "talk_btn"],
    "$hut_choices": ["enter_hut_btn", "continue_btn"],
    "$city_choices": ["merchant_btn", "inn_btn"],
    "$merchant_choices": ["buy_btn", "skip_btn"],
    "$inn_choices": ["wine_btn", "news_btn"],
    "$river_choices": ["boat_btn", "bridge_btn"],
    "$cave_choices": ["enter_btn", "skip_btn"]
}
STARTING_BUTTONS = []

KEY_WORDS = {
    "start": ["начать", "старт", "запуск", "поехали"],
    "stop": ["стоп", "выход", "закрыть", "остановить"],
    "help": ["помощь", "справка", "команды", "подсказка"],
    "prev": ["назад", "вернуться", "обратно"],
    "next": ["далее", "продолжить"],

    # Основные пути
    "forest": ["лес", "в лес", "налево", "деревья"],
    "city": ["город", "в город", "направо", "площадь"],
    "river": ["река", "к реке", "вода", "берег"],

    # Лес
    "fight": ["сразиться", "драться", "атаковать", "бой"],
    "talk": ["поговорить", "разговор", "общаться", "мир"],
    "hut": ["хижина", "дом"],
    "continue": ["дальше", "пройти", "идти дальше"],

    # Город
    "merchant": ["торговец", "купец", "продавец"],
    "inn": ["трактир", "кабак", "бар"],
    "buy": ["купить", "взять", "меч", "оружие"],
    "skip": ["нет", "отказаться", "не надо"],

    # В трактире
    "wine": ["вино", "пить", "напиток"],
    "news": ["новости", "спросить", "информация", "слухи"],

    # Река
    "boat": ["лодка", "плыть", "переплыть"],
    "bridge": ["мост", "перейти", "по мосту"],
    "cave": ["пещера", "зайти", "внутрь"],
}

IMAGES = images

DEBUG_LANGUAGE = "ru"
LANGUAGE = "ru"
SOURCE_TEXT = "command"
