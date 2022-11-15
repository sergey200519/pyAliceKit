from pyAlice.py_alice import PyAlice
from pyAlice.intents.intents import Intents
# from pyAlice.errors import KeyWordErrorD
from pyAlice.intents.date_time import DateTime
import json
import datetime
import time

import datetime

params = {
  "meta": {
    "locale": "ru-RU",
    "timezone": "UTC",
    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
    "interfaces": {
      "screen": {},
      "payments": {},
      "account_linking": {}
    }
  },
  "session": {
    "message_id": 4,
    "session_id": "4f6c4093-df75-4737-ae99-db3887ca767c",
    "skill_id": "b733709c-f360-446e-bbff-9627c569da64",
    "user": {
      "user_id": "41CD9AA328ADBF49138CAFF0F4952026ED6FB488F4DED151E52F0657C6A8C895"
    },
    "application": {
      "application_id": "5CBA8D4ACF747B45DCB05412FAEB90DCCE761184E1C4CDC9479A74EFB99D7C8A"
    },
    "user_id": "5CBA8D4ACF747B45DCB05412FAEB90DCCE761184E1C4CDC9479A74EFB99D7C8A",
    "new": False
  },
  "request": {
    "command": "помощь из раменского до выхино 15 мая 2022 года",
    "original_utterance": "алиса нужно твоя помощь",
    "nlu": {
      "tokens": [
        "привет"
      ],
      "entities": [],
      "intents": {
        "endintent": {
          "slots": {}
        },
        "all_intent": {
          "slots": {}
        }
      }
    },
    "markup": {
      "dangerous_context": False
    },
    "type": "SimpleUtterance"
  },
  "state": {
    "session": {},
    "user": {},
    "application": {}
  },
  "version": "1.0"
}

# with open("testing/settings.json", "r") as f:
#     settings = json.loads(f.read())
# print(settings)
start = datetime.datetime.now()
# a = PyAlice(new_settings="testing/settings", params_alice=params).get_params()
# print(a)
# print(f"events -> {a.events}")
# print(f"key_words -> {a.key_words}")
# print(f"intents -> {a.intents}")
# print(f"text -> {a.default_text}")
# print(f"buttons -> {a.buttons}")
settings = {
    "events": True,
    "debug": False,
    "buttons_dialogs_auto": True,
    "time_zone": None,
    "text_for_intents": "command",
    "text_for_key_words": "command",
    "version": "1.0",
    "error_dialog": "Я вас не поняла",
    "dialogs_file": "testing/dialogs",
    "intents_file": "testing/intents",
    "key_words_file": "testing/key_word",
    "buttons_file": "testing/buttons",
    "const_buttons": None,
    "language": "ru"
}
# a = DateTime("привет я прийду домой без 10 минут 10 часов", settings=settings)
# print(a.get_data())
# a = PyAlice()
# a = Intents(settings, "testing/intents", "из раменского до выхино в 14:00", start_time=datetime.datetime.now())
# print(a.logs())
# from pyAlice.testing_fr import fun
# fun()


def handler(event, context=""):
    a = PyAlice(new_settings="testing/settings", params_alice=event)
    events = a.get_events()
    buttons = a.get_buttons()
    key_words = a.get_key_words()
    intents = a.get_intents()
    print(f"events ---> {events}")
    print(f"buttons ---> {buttons}")
    print(f"key_words ---> {key_words}")
    print(f"intents ---> {intents}")
    a = a.get_params(text=a.text)
    # print(f"response text ---> {a['response']['text']}")
    # a["response"]["text"] = event["request"]["command"]
    return a
