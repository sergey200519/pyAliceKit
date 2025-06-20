import datetime, json
from types import ModuleType
from typing import Any, Optional, Self

from pyAliceKit.core.buttons import Buttons
from pyAliceKit.core.storage import Storage
from pyAliceKit.messages.embedded_message import embedded_message
from pyAliceKit.utils.errors.errors import SettingsErrors
from pyAliceKit.utils.settings_validation import new_settings_is_valid
from pyAliceKit.utils.terminal import clear_terminal, print_log, print_start_welcome


class Base:
    # bool
    new, end_session, inaction = False, False, True
    # str
    result_message, came_message = "", ""
    # dict
    intents = {}
    storage: Storage
    events = {}
    logs: dict[str, str] = {}
    more_data_message = {}
    # list
    buttons: Buttons
    alice_buttons: list[dict[str, Any]] = []
    key_words: "KeyWords" # type: ignore

    EMBEDDED_MESSAGE: dict[str, str] = embedded_message

    def __init__(self, params_alice: dict[Any, Any] | str, settings: ModuleType) -> None:
        self.start_time: datetime.datetime = datetime.datetime.now()

        self.params_alice: dict[Any, Any] = params_alice if isinstance(params_alice, dict) else json.loads(params_alice)

        settings_is_valid: str = new_settings_is_valid(settings)
        if settings_is_valid != "settings_is_valid":
            raise SettingsErrors(settings_is_valid, language=settings.DEBUG_LANGUAGE)
        
        self.settings: ModuleType = settings

        if self.settings.DEBUG:
            clear_terminal()
            print_start_welcome()

        #  Initialize options
        self.buttons = Buttons(self.settings)
        self.storage = Storage(self.settings)


    def add_log(self: Self, log: str, color: str | None = None, bg_color: Optional[str] = None, context: str = "", start_time: datetime.datetime = datetime.datetime.now()) -> None:
        if not self.settings.DEBUG:
            return
        delta_time: datetime.timedelta = datetime.datetime.now() - start_time
        time: str = f"{delta_time.seconds}s {delta_time.microseconds} micros"
        log_text: str = self.EMBEDDED_MESSAGE.get(f"{log}-{self.settings.DEBUG_LANGUAGE}", "").format(context)
        self.logs[time] = f"{log_text}"
        print_log(
            log_text,
            time,
            text_color=color,
            bg_color=bg_color
        )