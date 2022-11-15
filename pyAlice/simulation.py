import os
import json
from index import handler
import datetime

req = {
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
    "message_id": 0,
    "session_id": "2082b3f3-46a2-44d9-ae39-a461b565d62d",
    "skill_id": "b733709c-f360-446e-bbff-9627c569da64",
    "user": {
      "user_id": "41CD9AA328ADBF49138CAFF0F4952026ED6FB488F4DED151E52F0657C6A8C895"
    },
    "application": {
      "application_id": "5CBA8D4ACF747B45DCB05412FAEB90DCCE761184E1C4CDC9479A74EFB99D7C8A"
    },
    "user_id": "5CBA8D4ACF747B45DCB05412FAEB90DCCE761184E1C4CDC9479A74EFB99D7C8A",
    "new": True
  },
  "request": {
    "command": "",
    "original_utterance": "",
    "nlu": {
      "tokens": [],
      "entities": [],
      "intents": {}
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


req2 = {
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
    "message_id": 3,
    "session_id": "2082b3f3-46a2-44d9-ae39-a461b565d62d",
    "skill_id": "b733709c-f360-446e-bbff-9627c569da64",
    "user": {
      "user_id": "41CD9AA328ADBF49138CAFF0F4952026ED6FB488F4DED151E52F0657C6A8C895"
    },
    "application": {
      "application_id": "5CBA8D4ACF747B45DCB05412FAEB90DCCE761184E1C4CDC9479A74EFB99D7C8A"
    },
    "user_id": "5CBA8D4ACF747B45DCB05412FAEB90DCCE761184E1C4CDC9479A74EFB99D7C8A",
    "new": False,
  },
  "request": {
    "command": "",
    "original_utterance": "",
    "nlu": {
      "tokens": [],
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
      "dangerous_context": False,
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
with open("pyAlice/req.json", "r", encoding="utf-8") as f:
    req = json.loads(f.read())

with open("pyAlice/req2.json", "r", encoding="utf-8") as f:
    req2 = json.loads(f.read())


class Simulation:
    output = ""

    def __init__(self):
        self.simulation()

    def get_text(self, data):
        # print(data)
        # exit(0)
        text = f"{data['response']['text']}"
        temp = ""
        i = 0
        for item in text.split(" "):
            temp += item + " "
            if i > 10:
                self.output += temp + "\n"
                temp = ""
                i = 0
            else:
                i += 1
        if temp != "":
            self.output += temp + "\n"
        else:
            self.output += "\n"
        print(f"text --> {self.output}")
        self.output = ""

    def get_buttons(self, data):
        buttons = data["response"]["buttons"]
        first_buttons = []
        last_buttons = []
        for item in buttons:
            if not item["hide"]:
                first_buttons.append(item["title"])
                new = False
            else:
                last_buttons.append(item["title"])
        return [first_buttons, last_buttons]

    def view_buttons(self, buttons):
        first_buttons = buttons[0]
        last_buttons = buttons[1]
        for item in first_buttons:
            print("_" * 40)
            print(item)
        print("_" * 40)
        last_buttons_text1 = ""
        last_buttons_text2 = ""
        last_buttons_text3 = ""
        for item in last_buttons:
            n = len(item)
            last_buttons_text1 += " " + "_" * (n + 2) + " "
            last_buttons_text2 += f" |{item}| "
            last_buttons_text3 += " " + "‾" * (n + 2) + " "
        print(last_buttons_text1)
        print(last_buttons_text2)
        print(last_buttons_text3)

    def simulation(self):
        new = True
        while True:
            if new:
                start = datetime.datetime.now()
                data = json.loads(handler(req))
                end = datetime.datetime.now() - start
                self.get_text(data)
                buttons = self.get_buttons(data)
                self.view_buttons(buttons)
                status = ""
                if end.seconds < 1:
                    status = "Отлично"
                if end.seconds > 1 and end.seconds < 2:
                    status = "Хорошо"
                if end.seconds > 3:
                    status = "Очень плохо"
                print(f"Время отклика {end.seconds} секунд и {end.microseconds} милисекунд. {status}")
                # alice_params = req
                # input_text = input()
                # alice_params["request"]["command"] = input_text
                # alice_params["request"]["original_utterance"] = input_text
                # data = handler(alice_params)
                # self.get_text(data)
                # buttons = self.get_buttons(data)
                # self.view_buttons(buttons)
                new = False
                continue
            input_text = input()
            os.system('cls' if os.name == 'nt' else 'clear')
            if input_text == "q" or input_text == "finish" or input_text == "exit" or input_text == "end":
                break
            alice_params = req2
            alice_params["request"]["command"] = input_text
            alice_params["request"]["original_utterance"] = input_text
            start = datetime.datetime.now()
            data = json.loads(handler(alice_params))
            end = datetime.datetime.now() - start
            self.get_text(data)
            buttons = self.get_buttons(data)
            self.view_buttons(buttons)
            buttons = ""
            status = ""
            if end.seconds < 1:
                status = "Отлично"
            if end.seconds > 1 and end.seconds < 2:
                status = "Хорошо"
            if end.seconds > 3:
                status = "Очень плохо"
            print(f"Время отклика {end.seconds} секунд и {end.microseconds} милисекунд. {status}")
