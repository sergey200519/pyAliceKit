import datetime
import json
import pathlib

from pyAlice.functions import distribution_of_settings, get_buttons, open_json_file, new_settings_is_valid
from pyAlice.key_word import KeyWord
from pyAlice.intents.intents import Intents
from pyAlice.errors.base_errors import SettingsEroors, KeyWordsErrors, IntentsErrors
from pyAlice.base import Base


MAIN_DIR = pathlib.Path.cwd()

with open(f"{MAIN_DIR}/pyAlice/module_dialogs.json", "r") as f:
    module_dialogs_json = json.loads(f.read())


class PyAlice(Base):
    settings = {
        "events": True,
        "debug": True,
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
        "language": "en"
    }
    # bool
    # str
    default_text, key_words = "", ""
    # dict
    intents, dialogs = {}, {}
    # list
    events, buttons = [], []
    # other data type
    time_start_working = datetime.datetime.now()

    def __init__(self, params_alice, new_settings=None, now=None):
        if open_json_file(new_settings) == {}:
            raise SettingsEroors("settings_empty_error")
        self.time_start_working = datetime.datetime.now()
        self.params_alice = params_alice
        self.now = now
        is_valid = new_settings_is_valid(new_settings)
        if type(is_valid) != bool:
            raise SettingsEroors(is_valid)
        self.__configuration_options(new_settings)
        self.__processing_params()
    #
    def __configuration_options(self, settings):
        if settings == None:
            self.add_log("configuration_options_not_change_log")
            return ""
        try:
            new_settings = open_json_file(settings)
            self.settings = distribution_of_settings(self.settings, new_settings)
            self.add_log("configuration_options_log")
        except:
            self.add_log("configuration_options_log_error")

    def __is_text_in_params(self):
        request = self.params_alice["request"]
        if (request.get("command") == None or request.get("command") == "") and (request.get("original_utterance") == None or request.get("original_utterance") == ""):
            return False
        return True

    def __processing_params(self):
        if self.__is_text_in_params():
            text = self.params_alice["request"]
            try:
                key_word = KeyWord(self.settings.get("key_words_file"), text.get(self.settings.get("text_for_key_words")), MAIN_DIR).key_word()
                if key_word:
                    if not key_word.get("success"):
                        self.events.append("DuplicateKeyWordEvent")
                        self.add_log("key_word_duplicate_log")

                    else:
                        if key_word.get("event") != []:
                            self.events.extend(key_word.get("event"))
                        if key_word.get("dialog") != "":
                            self.default_text = key_word.get("dialog")
                        if key_word.get("buttons") != []:
                            self.buttons.extend(get_buttons(key_word.get("buttons"), self.settings.get("buttons_file")))
                        self.key_words = key_word.get("key_word")

                        self.add_log("key_word_log")
                else:
                    self.add_log("key_word_not_found_log")
            except KeyWordsErrors as exc:
                raise
            except:
                self.add_log("key_word_log_error")
            try:
                intents = Intents(self.settings, self.settings.get("intents_file"), text.get(self.settings.get("text_for_intents"))).get_intents_data()
                if intents["events"]:
                    self.events.extend(intents["events"])
                if intents["buttons"]:
                    self.buttons.extend(intents["buttons"])
                self.intents = intents.get("intents")
            except IntentsErrors as exc:
                raise
            except:
                raise
        else:
            self.add_log("not_text_log")



















#
