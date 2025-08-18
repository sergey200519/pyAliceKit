
import json
from typing import Any
from pyAliceKit.core.event_emitter import on_event
import settings
from pyAliceKit.py_alice.py_alice import PyAlice

params_alice: dict[Any, Any] = {
    "request": {
        "command": "Привет",
        "original_utterance": "Привет",
        "type": "SimpleUtterance",
        "nlu": {
            "tokens": ["привет, начать"],
            "entities": [],
            "intents": {}
        }
    },
    "session": {
        "message_id": 1,
        "session_id": "1234567890",
        "skill_id": "abcdefg1234567",
        "user_id": "user12345",
        "new": True,
        "application_id": "app12345"
    },
    "version": "1.0"
}
with open("testing/request4.json", "r", encoding="utf-8") as file:
    params_alice = json.load(file)

@on_event("storageFillEvent")
def hello(event: dict[str, Any], *args: Any, **kwargs: Any) -> None:
    """
    Обработчик события, который заполняет хранилище.
    """
    return
    print("Хранилище заполнено:", event)


@on_event("testEvent")
def test_event(event: dict[str, Any], *args: Any, **kwargs: Any) -> None:
    pass


alice: PyAlice = PyAlice(params_alice=params_alice, settings=settings)
print(alice.came_message) 
print(alice.key_words.key_words)  # type: ignore # Вывод ключевых слов, найденных в тексте
# print(alice.intents.intents)
# print(alice.events.get_events())
print(alice.dialogs.dialog, "<-------- index.py")  # type: ignore # Вывод текущего диалога
# print(alice.get_params_for_alice()) 
print(alice.buttons.current_buttons)  # type: ignore # Вывод кнопок, доступных в текущем диалоге
# print(settings.DIALOG_NODES)