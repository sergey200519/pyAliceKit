import datetime
import json
import pathlib

from module.functions import distribution_of_settings, get_buttons, open_json_file, new_settings_is_valid
from module.key_word import KeyWord
from module.errors import KeyWordErrorD
from module.base import Base


MAIN_DIR = pathlib.Path.cwd()


class PyAlice(Base):
    def __init__(self, params_alice, new_settings=None, now=None):
        self.time_start_working = datetime.datetime.now()
        self.params_alice = params_alice
        self.now = now
        is_valid = new_settings_is_valid(new_settings)
        if is_valid == True and not self.stop_work:
            self.__configuration_options(new_settings)
            self.__processing_params()
        else:
            self.add_log(is_valid)
            self.stop_work = True

    def __configuration_options(self, settings):
        if settings == None:
            self.add_log("configuration_options_not_change_log")
            return ""
        try:
            self.settings = distribution_of_settings(self.settings, open_json_file(settings))
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
            try:
                text = self.params_alice["request"]
                key_word = KeyWord(self.settings.get("key_words_file"), text.get(self.settings.get("text_for_key_word")), MAIN_DIR).key_word()
                if key_word:
                    if not key_word.get("success"):
                        self.events.append("DuplicateKeyWordEvent")
                        self.add_log("key_word_duplicate_log")

                    else:
                        if key_word.get("event") != "":
                            self.events.append(key_word.get("event"))
                        if key_word.get("dialog") != "" and self.settings["buttons_dialogs_auto"]:
                            self.default_text = key_word.get("dialog")
                        if key_word.get("buttons") != []:
                            self.buttons.extend(get_buttons(key_word.get("buttons"), self.settings.get("buttons_file")))
                        self.key_word = key_word.get("key_word")

                        self.add_log("key_word_log")
                else:
                    self.add_log("key_word_not_found_log")
                print(key_word)
            except:
                self.add_log("key_word_log_error")
        else:
            self.add_log("not_text_log")

















#
