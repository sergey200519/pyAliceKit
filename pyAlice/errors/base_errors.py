import pathlib
import json

MAIN_DIR = pathlib.Path.cwd()

with open(f"{MAIN_DIR}/pyAlice/errors/errors_dialogs.json", "r") as f:
    errors_dialogs_json = json.loads(f.read())

with open(f"{MAIN_DIR}/pyAlice/module_dialogs.json", "r") as f:
    module_dialogs_json = json.loads(f.read())


class BaseErrors(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.msg = args[0] if args else None

    def get_dialog(self, key):
        if "$" in key:
            return module_dialogs_json.get(key.replace("$", ""))
        elif "#" in key:
            return key.replace("#", "")
        else:
            return errors_dialogs_json.get(key)


class SettingsEroors(BaseErrors):
    def __str__(self):
        return f"Settings Error: {self.get_dialog(self.msg)}"


class KeyWordsErrors(BaseErrors):
    def __str__(self):
        return f"Key words Error: {self.get_dialog(self.msg)}"


class IntentsErrors(BaseErrors):
    def __str__(self):
        return f"Intents Error: {self.get_dialog(self.msg)}"
