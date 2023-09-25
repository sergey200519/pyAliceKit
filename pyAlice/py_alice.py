"""
PyAlice
v0.1
"""



import datetime
import json
import os
from pathlib import Path


from pyAlice.base import Base
from pyAlice.key_word import KeyWord
from pyAlice.errors.errors import SettingsErrors, KeyWordsErrors
from pyAlice.functions import new_settings_is_valid, clear_console, pass_fun, finish_PyAlice


class PyAlice(Base):
    def __init__(self, params_alice, settings, time_now=datetime.datetime.now(), \
                 distributor=finish_PyAlice, emptiness_actions=pass_fun, successful_fun=pass_fun):
        clear_console()
        self.params_alice = params_alice if type(params_alice) is dict else json.loads(params_alice)
        self.time_now = time_now
        self.start_time = datetime.datetime.now()

        settings_is_valid = new_settings_is_valid(settings)
        if settings_is_valid != "success":
            raise SettingsErrors(settings_is_valid, language=settings.DEBUG_LANGUAGE)
        self.settings = settings
        self.add_log("configuration_options_log", color="yellow", start_time=self.start_time)

        self.end_session = False
        self.inaction = True

        self.__processing_params()
        return distributor(self, emptiness_actions, successful_fun)

    def init_key_word(self):
        try:
            text_for_key_words = self.params_alice["request"][self.settings.TEXT_FOR_KEY_WORDS]
            key_words = KeyWord(text=text_for_key_words, settings=self.settings, start_time=self.start_time).key_word()

            if key_words["key_words"] == []:
                self.add_log("key_word_not_found_log", color="green", start_time=self.start_time)
            else:
                self.key_word = key_words["key_words"]
                for item in key_words["messages"]:
                    if item != "$NULL":
                        if self.result_message != "":
                            old_message = self.result_message
                            # self.result_message = self.get_message(item)
                            self.add_message(item)
                            self.add_event({
                                "event": "overwritingDefaultTextEvent",
                                "old_message": old_message,
                                "new_message": self.result_message
                                }, "KeyWord")
                        else:
                            # self.result_message = self.get_message(item)
                            self.add_message(item)
                for item in key_words["events"]:
                    self.add_event({"event":item}, "KeyWord")
                # self.buttons.extend(key_words["buttons"])
                self.add_buttons(key_words["buttons"])
                self.add_log("key_word_log", color="green", start_time=self.start_time)
        except KeyWordsErrors as exc:
            raise


    def __processing_params(self):
        self.text = self.params_alice["request"][self.settings.SOURCE_TEXT]
        self.new = self.params_alice["session"]["new"]

        self.intents = self.params_alice["request"]["nlu"]["intents"]

        if self.params_alice.get("state") is not None:
            self.storage = self.params_alice["state"]["session"]
            self.add_log("storage_fill", color="green", start_time=self.start_time)
            self.add_event({
                            "event": "storageFillEvent",
                            "storage": self.storage
                            }, "__init__")
        else:
            self.add_log("storage_not_fill", color="yellow", start_time=self.start_time)
        
        if self.new:
            # self.result_message = self.settings.ALL_MESSAGES[self.settings.STARTING_MESSAGE]
            self.add_message(self.settings.STARTING_MESSAGE)
            self.add_buttons(self.settings.STARTING_BUTTONS)
            self.add_log("first_starting_end", color="green", start_time=self.start_time)
            return
        
        self.init_key_word()
        self.alice_buttons = self.get_buttons()

    def get_params_for_alice(self, type="json"):
        params_for_alice = {
            "state": {
                "session": self.storage
            },
            "session_state": self.storage,
            'version': self.params_alice['version'],
            'session': self.params_alice['session'],
            'response': {
                "buttons": self.alice_buttons,
                # Respond with the original request or welcome the user if this is the beginning of the dialog and the request has not yet been made.
                'text': self.result_message,
                # Don't finish the session after this response.
                'end_session': self.end_session
            },
        }
        if self.more_data_message != {}:
            for key, value in self.more_data_message.items():
                params_for_alice["response"][key] = value
        if type == "json":
            return json.dumps(params_for_alice)
        elif type == "dict":
            return params_for_alice
    
    def end_session_alice(self):
        self.end_session = True
        self.add_log("session_end", color="purple", start_time=self.start_time)


    




#