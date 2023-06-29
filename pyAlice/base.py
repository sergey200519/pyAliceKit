import datetime

from pyAlice.messages.embedded_message import embedded_message
from pyAlice.errors.base_errors import MessageErrors


class Base:
    # bool
    new = False
    # str
    default_text, key_word, text = "", "", ""
    # dict
    intents, message, buttons_dict, storage, events, logs = {}, {}, {}, {}, {}, {}
    # list
    buttons = []

    EMBEDDED_MESSAGE = embedded_message

    def add_log(self, log, color=None, correction="", start_time=datetime.datetime.now()):
        if not self.settings.DEBUG:
            return
        time = str(datetime.datetime.now() - start_time)[5:]
        log_text = self.EMBEDDED_MESSAGE.get(f"{log}-{self.settings.MESSAGE_DEBUG_LANGUAGE}")
        self.logs[time] = f"{log_text} {correction}"
        if self.settings.LOG_OUTPUT_IMMEDIATELY:
            colors = {
                "black": "30",
                "red": "31",
                "green": "32",
                "yellow": "33",
                "blue": "34",
                "purple": "35",
                "turquoise": "36",
                "white": "37"
            }
            if color is not None:
                color_str = f"\033[{colors.get(color)}m"
                print(f"{color_str}{time} {log_text} {correction}\033[0m")
            else:
                print(f"{time} {log_text} {correction}")

    def get_message(self, message):
        answer = self.settings.MESSAGE.get(message)
        if answer is None:
            raise MessageErrors("dialog_not_found_error", context=message, language=self.settings.MESSAGE_DEBUG_LANGUAGE)
        return answer
