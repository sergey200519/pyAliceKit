from types import ModuleType
from typing import Any, Self
from pyAliceKit.base import Base
from pyAliceKit.core.dialog_engine import DialogEngine
from pyAliceKit.core.event_emitter import event_emitter
from pyAliceKit.core.intents import Intents
from pyAliceKit.core.key_words import KeyWords
from pyAliceKit.core.session_storage import SessionStorage
from pyAliceKit.utils.errors.errors import IntentsErrors, KeyWordsErrors, SettingsErrors, StorageErrors
from pyAliceKit.utils.tools import from_str_bool_to_py_bool


class PyAlice(Base):
    """
    PyAlice is a class that initializes the Alice API with the provided parameters and settings.
    It sets up various attributes related to the session, such as intents, storage, and buttons.
    """

    def __init__(self: Self, params_alice: dict[Any, Any] | str, settings: ModuleType) -> None:
        super().__init__(params_alice, settings)
        self.add_log("configuration_options_log", color="yellow", start_time=self.start_time)
        self.__processing_params()
        self.dialogs = DialogEngine(
            settings=self.settings,
            pyAlice=self
        )
        self.dialogs.find_best_dialog()


    def init_key_word(self):
        try:

            if self.settings.TEXT_FOR_KEY_WORDS in self.params_alice["request"]:
                text_for_key_words = self.params_alice["request"][self.settings.TEXT_FOR_KEY_WORDS]
            elif "nlu" in self.params_alice["request"]:
                text_for_key_words = " ".join(self.params_alice["request"]["nlu"]["tokens"])
            else:
                text_for_key_words = ""

           
            self.key_words: KeyWords = KeyWords(
                text=text_for_key_words,
                settings=self.settings
            )
            self.add_log("key_word_init_log", color="purple", start_time=self.start_time)
            self.key_words.key_word()
            if self.key_words.key_words != []:
                self.add_log("key_word_log", color="purple", start_time=self.start_time)
            else:
                self.add_log("key_word_not_found_log", color="purple", start_time=self.start_time)

        except KeyWordsErrors:
            raise

        try:
            self.intents: Intents = Intents(
                params_alice=self.params_alice,
                settings=self.settings
            )
            self.add_log("intents_log", color="blue", start_time=self.start_time)
        except IntentsErrors:
            raise

    
    def __processing_params(self: Self) -> None:
        if self.settings.SOURCE_TEXT in self.params_alice["request"].keys():
            self.came_message = self.params_alice["request"][self.settings.SOURCE_TEXT]
        elif "nlu" in self.params_alice["request"].keys():
            self.came_message = " ".join(self.params_alice["request"]["nlu"]["tokens"])
        else:
            self.came_message = ""

        temp_new: bool | int = from_str_bool_to_py_bool(self.params_alice["session"]["new"])
        if temp_new != -1:
            self.new = temp_new
        else:
            raise SettingsErrors("new_boolean_setting_error", language=self.settings.DEBUG_LANGUAGE)
        
        self.session_storage = SessionStorage(
            params_alice=self.params_alice,
            settings=self.settings
        )
        if self.session_storage.get_all() != {}:
            self.add_log("storage_fill", color="green", start_time=self.start_time)
            event_emitter.emit(event_name="storageFillEvent", event={
                                                                "event": "storageFillEvent",
                                                                "where": "PyAlice.__processing_params",
                                                                "cls": self,
                                                                "storage": self.session_storage
                                                                })
        else:
            self.add_log("storage_not_fill", color="light_red", start_time=self.start_time)
            event_emitter.emit(event_name="storageNotFillEvent", event={
                                                                "event": "storageNotFillEvent",
                                                                "where": "PyAlice.__processing_params",
                                                                "cls": self,
                                                                "storage": self.session_storage
                                                                })
        
        try:
            self.previous_dialogue = self.session_storage.get("pyAliceKit").get("previous_dialogue")
        except StorageErrors:
            self.previous_dialogue = None
        except Exception:
            self.previous_dialogue = None


        self.init_key_word()
