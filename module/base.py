import datetime
import pathlib
import json

MAIN_DIR = pathlib.Path.cwd()

with open(f"{MAIN_DIR}/module/module_dialogs.json", "r") as f:
    module_dialogs_json = json.loads(f.read())


class Base:
    settings = {
        "events": True,
        "debug": True,
        "buttons_dialogs_auto": True,
        "time_zone": None,
        "text_for_intents": "command",
        "text_for_key_word": "command",
        "version": "1.0",
        "error_dialog": "Я вас не поняла",
        "dialogs_file": "dialogs",
        "intents_file": "intents",
        "key_words_file": "key_word",
        "buttons_file": "buttons",
        "const_buttons": None
    }
    # bool
    stop_work = False
    # str
    default_text, key_word = "", ""
    # dict
    intents, logs_dict, dialogs, logs_dict = {}, {}, {}, {}
    # list
    events, buttons = [], []
    # other data type
    module_dialogs = module_dialogs_json
    time_start_working = datetime.datetime.now()

    def add_log(self, log, correction="", start_time=datetime.datetime.now()):
        if not self.settings.get("debug"):
            return ""
        time = datetime.datetime.now() - start_time
        self.logs_dict[str(time)[5:]] = f"{self.module_dialogs.get(log)} {correction}"

    def logs(self):
        if not self.settings.get("debug"):
            return self.module_dialogs.get("change_debug")
        answer = ""
        for key, value in self.logs_dict.items():
            answer += f"{key} {value}\n"
        return answer











#
