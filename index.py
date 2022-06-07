from module.py_alice import PyAlice
from module.intents import Intents
from module.errors import KeyWordErrorD
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
    "command": "алиса нужно твоя помощь",
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
# a = PyAlice(new_settings="testing/settings", params_alice=params)
#
#
#
# print(a.logs())
# print(a.events)
# print(a.key_word)
# print(a.default_text)
# print(a.buttons)
a = Intents("testing/intents", "из раменского до выхино в 14:00", start_time=datetime.datetime.now())
print(a.logs())

#
