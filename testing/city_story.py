from typing import Any

from pyAliceKit.py_alice.py_alice import PyAlice
from pyAliceKit.utils.dialogs import include_nodes


city_story = include_nodes({
    "message": "city_start",
    "buttons": ["$city_choices"],
    "childs": {
        "merchant": {
            "message": "city_merchant",
            "buttons": ["$merchant_choices"],
            "childs": {
                "buy": {
                    "message": "Ты купил меч. Теперь ты вооружён!",
                    "transitions": ["/river"]
                },
                "skip": {
                    "message": "Ты отказался от меча и пошёл дальше.",
                    "transitions": ["/river"]
                }
            }
        },
        "inn": {
            "message": "city_inn",
            "buttons": ["$inn_choices"],
            "childs": {
                "wine": {
                    "message": "city_wine",
                    "end_dialog": True
                },
                "news": {
                    "message": "city_news",
                    "transitions": ["/forest", "/river"]
                }
            }
        }
    }
}, True)