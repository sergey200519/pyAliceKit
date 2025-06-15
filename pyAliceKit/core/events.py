from types import ModuleType
from typing import Self


class Events:
    def __init__(self: Self, settings: ModuleType) -> None:
        self.__settings: ModuleType = settings
        self.events = {}