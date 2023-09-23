import os
from sys import platform

from pyAlice.functions import clear_console


class Simulation:
    def __init__(self, handler):
        clear_console()
        self.handler = handler
        self.user_data = ""
        self.response()

    def request(self):
        self.user_data = input()
        return self.handler({
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
                "message_id": 5,
                "session_id": "5175cbbd-e484-4858-b253-f4c7b4632385",
                "skill_id": "37ccbb22-0b07-4a93-85c0-8517d17ccda7",
                "user": {
                    "user_id": "150725BC0540B5EDE3E831A6DB9EFA4F5A3E9BD8BD7F800301393F537B2D40E6"
                },
                "application": {
                    "application_id": "EA141820AAB4284BCD741A1D9037A49D06166D2141AAE685F9360C6DEF2853B7"
                },
                "new": False,
                "user_id": "EA141820AAB4284BCD741A1D9037A49D06166D2141AAE685F9360C6DEF2853B7"
            },
            "request": {
                "command": f"{self.user_data}",
                "original_utterance": f"{self.user_data}",
                "nlu": {
                    "tokens": [item for item in self.user_data.split(" ")],
                    "entities": [],
                    "intents": {}
                },
                "markup": {
                    "dangerous_context": False
                },
                "type": "SimpleUtterance"
            },
            "version": "1.0"
        })

    def response(self):
        while True:
            req = self.request()
            print(req["response"]["text"])
            if req["response"]["end_session"] == True:
                exit()
