from types import ModuleType
from typing import Any, Self
from pyAliceKit.base import Base
from pyAliceKit.core.event_emitter import event_emitter
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
        
        if self.params_alice.get("state") is not None:
            
            self.storage.set_storage("state", self.params_alice["state"], overwrite=True)
            self.add_log("storage_fill", color="green", start_time=self.start_time)
            event_emitter.emit(event_name="storageFillEvent", event={
                                                                    "event": "storageFillEvent",
                                                                    "where": "PyAlice.__processing_params",
                                                                    "cls": self,
                                                                    "storage": self.storage
                                                                    })
        else:
            self.add_log("storage_not_fill", color="yellow", start_time=self.start_time)
