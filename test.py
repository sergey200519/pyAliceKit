def test():

    return {
        "state": {
            "session": {}
        },
        "session_state": {},
        "version": "1.0",
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
            "new": "false",
            "user_id": "EA141820AAB4284BCD741A1D9037A49D06166D2141AAE685F9360C6DEF2853B7"
        },
        "response": {
            "buttons": [
                {
                    "title": "full_search",
                    "payload": {
                        "title": "full_search"
                    },
                    "hide": "true"
                },
                {
                    "title": "fast_search",
                    "payload": {
                        "title": "fast_search"
                    },
                    "hide": "true"
                },
                {
                    "title": "help",
                    "payload": {
                        "title": "help"
                    },
                    "hide": "true"
                }
            ],
            "text": "Вы на веpном пути",
            "end_session": "false"
        }
    }


print(test())
