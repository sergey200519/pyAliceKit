import datetime
import pathlib
import json

MAIN_DIR = pathlib.Path.cwd()

with open(f"{MAIN_DIR}/pyAlice/module_dialogs.json", "r") as f:
    module_dialogs_json = json.loads(f.read())


class Base:
    logs_dict = {}
    module_dialogs = module_dialogs_json

    def add_log(self, log, correction="", start_time=datetime.datetime.now()):
        if not self.settings.get("debug"):
            return ""
        time = datetime.datetime.now() - start_time
        if self.settings.get("language") == "ru":
            req = log
        else:
            req = f"{log}-{self.settings['language']}"
        self.logs_dict[str(time)[5:]] = f"{self.module_dialogs.get(req)} {correction}"

    def logs(self):
        if not self.settings.get("debug"):
            return self.module_dialogs.get("change_debug")
        answer = ""
        for key, value in self.logs_dict.items():
            answer += f"{key} {value}\n"
        return answer











#
