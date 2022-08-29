import datetime
import pathlib
import json
from pyAlice.errors.base_errors import BaseErrors

MAIN_DIR = pathlib.Path.cwd()

with open(f"{MAIN_DIR}/pyAlice/module_dialogs.json", "r") as f:
    module_dialogs_json = json.loads(f.read())

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

backgrounds = {
    "black": "40",
    "red": "41",
    "green": "42",
    "yellow": "43",
    "blue": "44",
    "purple": "45",
    "turquoise": "46",
    "white": "47"
}

colors_for_pyAlice = {
    "main": colors.get("yellow"),
    "key_words": colors.get("green"),
    "intents": colors.get("turquoise"),
    "date_time": colors.get("purple"),
    "warning": colors.get("yellow"),
    "error": colors.get("red")
}


class Base:
    logs_dict = {}
    module_dialogs = module_dialogs_json

    def add_log(self, log, correction="", start_time=datetime.datetime.now(), color=None, background=None, type=None):
        if not self.settings.get("debug"):
            return ""
        if color is not None and type is not None:
            raise BaseErrors("color_logs_error")
        time = datetime.datetime.now() - start_time
        if self.settings.get("language") == "ru":
            req = log
        else:
            req = f"{log}-{self.settings['language']}"
        if self.settings.get("log_output_immediately") and type:
            background = f"\033[{backgrounds.get(background)}m" if background is not None else ""
            color = f"\033[{colors_for_pyAlice.get(type)}m" if type is not None else ""
            print(f"{color}{background}{str(time)[5:]} {self.module_dialogs.get(req)} {correction}\033[0m")
        elif self.settings.get("log_output_immediately"):
            background = f"\003[{backgrounds.get(background)}m" if background else ""
            color = f"\033[{colors.get(color)}m" if color else ""
            print(f"{color}{background}{str(time)[5:]} {self.module_dialogs.get(req)} {correction}\033[0m")
        self.logs_dict[str(time)[5:]] = f"{self.module_dialogs.get(req)} {correction}"

    def logs(self):
        if not self.settings.get("debug"):
            return self.module_dialogs.get("change_debug")
        answer = ""
        for key, value in self.logs_dict.items():
            answer += f"{key} {value}\n"
        return answer











#
