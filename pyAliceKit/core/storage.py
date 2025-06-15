from types import ModuleType
from typing import Any, Self

from pyAliceKit.utils.errors.errors import StorageErrors


class Storage:
    def __init__(self: Self, settings: ModuleType) -> None:
        self.__settings: ModuleType = settings
        self.__storage: dict[Any, Any] = {}

    def get_storage(self: Self) -> dict[Any, Any]:
        return self.__storage
    
    def get_storage_by_key(self: Self, key: str) -> Any:
        data = self.__storage.get(key)
        if data is None:
            raise StorageErrors("item_in_storage_not_found_error", context=key, language=self.__settings.DEBUG_LANGUAGE)
        return data
    
    def set_storage(self, key: Any, data: Any, overwrite: bool = True) -> None:
        if key in self.__storage.keys() and not overwrite:
            raise StorageErrors("overwrite_storage_error", context=key, language=self.__settings.DEBUG_LANGUAGE)
        self.__storage[key] = data
    
    def update_storage_by_key(self, key: Any, data: Any) -> None:
        if key not in self.__storage.keys():
            raise StorageErrors("item_in_storage_not_found_error", context=key, language=self.__settings.DEBUG_LANGUAGE)
        self.__storage[key] = data