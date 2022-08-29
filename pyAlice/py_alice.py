import datetime
import json
import pathlib

from pyAlice.functions import distribution_of_settings, get_buttons, open_json_file, new_settings_is_valid, get_dialog
from pyAlice.key_word import KeyWord
from pyAlice.intents.intents import Intents
from pyAlice.errors.base_errors import SettingsEroors, KeyWordsErrors, IntentsErrors, PyAliceErrors
from pyAlice.base import Base


MAIN_DIR = pathlib.Path.cwd()

with open(f"{MAIN_DIR}/pyAlice/module_dialogs.json", "r") as f:
    module_dialogs_json = json.loads(f.read())


class PyAlice(Base):
    settings = {
        "events": True,
        "debug": True,
        "log_output_immediately": True,
        "buttons_dialogs_auto": True,
        "time_zone": None,
        "text_for_intents": "command",
        "text_for_key_words": "command",
        "version": "1.0",
        "error_dialog": "Я вас не поняла",
        "dialogs_file": "",
        "intents_file": "",
        "key_words_file": "",
        "buttons_file": "",
        "const_buttons": None,
        "language": "en",
        "starting_dialog": None,
        "source_text": "command"
    }
    # bool
    new = False
    # str
    default_text, key_words, text = "", "", ""
    # dict
    intents, dialogs, buttons_dict, storage = {}, {}, {}, {}
    # list
    events, buttons = [], []
    # other type data
    time_start_working = datetime.datetime.now()

    def __init__(self, params_alice, new_settings=None, now=None):
        self.buttons = []
        if open_json_file(new_settings) == {}:
            raise SettingsEroors("settings_empty_error")
        self.time_start_working = datetime.datetime.now()
        self.params_alice = params_alice
        self.now = now
        self.new = self.is_new(params_alice)
        self.text = self.params_alice["request"].get(self.settings.get("source_text"))
        is_valid = new_settings_is_valid(new_settings)
        if type(is_valid) != bool:
            raise SettingsEroors(is_valid)
        self.__configuration_options(new_settings)
        self.dialogs = open_json_file(self.settings.get("dialogs_file"))
        if self.new:
            self.default_text = get_dialog(self.dialogs, self.settings.get("starting_dialog"))
        self.text = self.params_alice["request"].get(self.settings.get("source_text"))
        self.buttons_dict = open_json_file(self.settings.get("buttons_file"))
        self.const_buttons = [item.strip() for item in self.settings.get("const_buttons").split(',')]
        self.params_for_alice = {}
        self.__processing_params()

    def __configuration_options(self, settings):
        if settings is None:
            self.add_log("configuration_options_not_change_log", start_time=self.time_start_working, type="main")
            return ""
        try:
            new_settings = open_json_file(settings)
            self.settings = distribution_of_settings(self.settings, new_settings)
            self.add_log("configuration_options_log", start_time=self.time_start_working, type="main")
        except Exception:
            self.add_log("configuration_options_log_error", start_time=self.time_start_working, type="main")

    def __is_text_in_params(self):
        request = self.params_alice["request"]
        if (request.get("command") is None or request.get("command") == "") and (request.get("original_utterance") is None or request.get("original_utterance") == ""):
            return False
        return True

    def is_new(self, params_alice):
        if params_alice["session"]["new"]:
            return True
        else:
            return False

    def __processing_params(self):
        if self.__is_text_in_params():
            text = self.params_alice["request"]
            # try:
            key_word = KeyWord(self.settings.get("key_words_file"), text.get(self.settings.get("text_for_key_words")), MAIN_DIR, settings=self.settings, start_time=self.time_start_working).key_word()
            if key_word:
                if not key_word.get("success"):
                    self.events.append("DuplicateKeyWordEvent")
                    self.add_log("key_word_duplicate_log", start_time=self.time_start_working, type="error")

                else:
                    if key_word.get("event") != []:
                        self.events.extend(key_word.get("event"))
                    if key_word.get("dialog") != "":
                        self.default_text = get_dialog(self.dialogs, key_word.get('dialog'))
                    if key_word.get("buttons") != []:
                        self.buttons.extend(key_word.get("buttons"))
                    self.key_words = key_word.get("key_word")
                    self.add_log("key_word_log", start_time=self.time_start_working, type="key_words")
            else:
                self.add_log("key_word_not_found_log", start_time=self.time_start_working, type="key_words")
            # except KeyWordsErrors as exc:
            #     raise
            # except Exception:
            #     self.add_log("key_word_log_error", start_time=self.time_start_working, type="error")
            try:
                intents = Intents(self.settings, self.settings.get("intents_file"), text.get(self.settings.get("text_for_intents")), start_time=self.time_start_working).get_intents_data()
                if intents["events"]:
                    self.events.extend(intents["events"])
                if intents["buttons"]:
                    self.buttons.extend(intents["buttons"])
                self.intents = intents.get("intents")
            except IntentsErrors as exc:
                raise
            except Exception:
                raise
        else:
            self.add_log("not_text_log")

    def get_params(self, text=None, end_session=False, type="json"):
        types = ["json", "dict"]
        if type not in types:
            raise PyAliceErrors("get_params_type_error")
        buttons_obj = []
        buttons = self.const_buttons
        buttons.extend(self.buttons)
        for item in buttons:
            for key, value in self.buttons_dict.items():
                if item.strip() == key.strip():
                    # print(f"{item} -> {value}")
                    buttons_obj.append(value)
                    break
        answer = {
            "state": {
                "session": self.storage
            },
            "session_state": self.storage,
            'version': self.settings.get("version"),
            'session': "",
            'response': {
                "buttons": buttons_obj,
                'text': self.default_text if self.default_text != "" else text,
                'end_session': False if not end_session else True
            },
        }
        if type == "json":
            return json.dumps(answer)
        elif type == "dict":
            return answer


#
