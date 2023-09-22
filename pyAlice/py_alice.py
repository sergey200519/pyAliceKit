import datetime

from pyAlice.base import Base
from pyAlice.functions import new_settings_is_valid
from pyAlice.errors.base_errors import SettingsEroors, KeyWordsErrors, IntentsErrors, PyAliceErrors
from pyAlice.messages.reasons import reasons
from pyAlice.key_word import KeyWord


class PyAlice(Base):
    def __init__(self, params_alice, settings, now=datetime.datetime.now()):
        self.params_alice = params_alice
        self.start_time = now

        settings_is_valid = new_settings_is_valid(settings)
        if type(settings_is_valid) != bool:
            raise SettingsEroors(settings_is_valid, language=settings.LANGUAGE)
        self.settings = settings
        self.add_log("configuration_options_log", color="yellow", start_time=self.start_time)

        self.text = self.params_alice["request"][self.settings.SOURCE_TEXT]

        self.__processing_params()

    def __get_reasons(self, name):
        return reasons.get(f"{name}-{self.settings.MESSAGE_DEBUG_LANGUAGE}")

    def key_word(self):
        try:
            text_for_key_words = self.params_alice["request"][self.settings.TEXT_FOR_KEY_WORDS]
            key_words = KeyWord(text=text_for_key_words, settings=self.settings, start_time=self.start_time).key_word()
            # Если поиск прошол удачно
            if not key_words:
                self.add_log("key_word_not_found_log", color="green", start_time=self.start_time)
            else:
                self.key_word = key_words["key_word"]
                if key_words["message"] != "$NULL":
                    if self.default_text != "":
                        self.events["overwriting_default_text_event"] = {
                            "where": "KeyWord",
                            "when": str(datetime.datetime.now() - self.start_time)[5:],
                            "reason": self.__get_reasons("overwriting_default_text_event_resons")
                        }
                    self.default_text = self.get_message(key_words["message"])
                if key_words["event"] != "$NULL":
                    self.events[key_words["event"]] = {
                        "where": "KeyWord",
                        "when": str(datetime.datetime.now() - self.start_time)[5:],
                        "reason": self.__get_reasons("from_key_words_event_resons")
                    }
                self.buttons.extend(key_words["buttons"])
                self.add_log("key_word_log", color="green", start_time=self.start_time)
        except KeyWordsErrors as exc:
            raise

    def __processing_params(self):
        self.key_word()
#
