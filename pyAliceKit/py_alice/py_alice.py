from types import ModuleType
from typing import Any, Self
from pyAliceKit.base import Base
from pyAliceKit.core.dialog_engine import DialogEngine
from pyAliceKit.core.event_emitter import event_emitter
from pyAliceKit.core.session_storage import SessionStorage
from pyAliceKit.py_alice.processors.keyword_and_intents import processing_keyword_and_intents
from pyAliceKit.utils.errors.errors import SettingsErrors
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
    
    def __processing_params(self: Self) -> None:
        self.__get_came_message()

        self.__processing_new()
        
        self.__processing_storage()
        
        self.__processing_service_storage()
        
        processing_keyword_and_intents(self)


    def __get_came_message(self: Self) -> None:
        if self.settings.SOURCE_TEXT in self.params_alice["request"].keys():
            self.came_message = self.params_alice["request"][self.settings.SOURCE_TEXT]
        elif "nlu" in self.params_alice["request"].keys():
            self.came_message = " ".join(self.params_alice["request"]["nlu"]["tokens"])
        else:
            self.came_message = ""

    def __processing_new(self: Self) -> None:
        temp_new: bool | int = from_str_bool_to_py_bool(self.params_alice["session"]["new"])
        if temp_new != -1:
            self.new = temp_new
        else:
            raise SettingsErrors("new_boolean_setting_error", language=self.settings.DEBUG_LANGUAGE)

    def __processing_storage(self: Self) -> None:
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
    
    def __processing_service_storage(self: Self) -> None:
        if self.new:
            self.previous_dialogue = "/"
        else:
            try:
                self.previous_dialogue = self.session_storage.get_service_storage().get("previous_dialogue", "/")
            except Exception as e:
                raise SettingsErrors("previous_dialogue_error", context=str(e), language=self.settings.DEBUG_LANGUAGE)