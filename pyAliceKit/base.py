import datetime, json
from types import ModuleType
from typing import Any

from pyAliceKit.messages.embedded_message import embedded_message
from pyAliceKit.utils.settings_validation import new_settings_is_valid
# from pyAlice.errors.errors import SettingsErrors, StorageErrors, MessageErrors

# from pyAlice.messages.embedded_message import embedded_message


class Base:
    # bool
    new, end_session, inaction = False, False, True
    # str
    result_message, came_message = "", ""
    # dict
    intents, storage, events, logs, more_data_message = {}, {}, {}, {}, {}
    # list
    buttons, alice_buttons, key_words = [], [], []

    EMBEDDED_MESSAGE: dict[str, str] = embedded_message

    def __init__(self, params_alice: dict[Any, Any] | str, settings: ModuleType) -> None:
        self.params_alice = params_alice if isinstance(params_alice, dict) else json.loads(params_alice)
        self.start_time = datetime.datetime.now()

        settings_is_valid: str = new_settings_is_valid(settings)
        if settings_is_valid != "settings_is_valid":
            pass
            # raise SettingsErrors(settings_is_valid, language=settings.DEBUG_LANGUAGE)
        self.settings = settings

