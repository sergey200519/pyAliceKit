import re
import datetime
from types import ModuleType
from typing import Any, Self

from pyAliceKit.base import Base
from pyAliceKit.utils.errors.errors import KeyWordsErrors

# FIXME: Without Base class
class KeyWords(Base):
    def __init__(self: Self, text: str, settings: ModuleType, start_time: datetime.datetime) -> None:
        # super().__init__({}, settings)
        self.text: str = text.lower()
        self.settings: ModuleType = settings
        self.start_time: datetime.datetime = start_time
        self.key_words_map: dict[str, list[str]] = settings.KEY_WORDS
        self.key_words: list[str] = []

        if self.settings.DEBUG:
            self._validate_key_words()
        self.add_log("key_word_init_log", color="green", start_time=self.start_time)

    def _validate_key_words(self: Self) -> None:
        all_words: dict[str, Any] = {}
        for intent, words in self.key_words_map.items():
            for word in words:
                word_lc = word.lower()
                if word_lc in all_words:
                    raise KeyWordsErrors("duplicate_keyword", context=f"'{word_lc}' используется в '{intent}' и '{all_words[word_lc]}'", language=self.settings.DEBUG_LANGUAGE)
                all_words[word_lc] = intent

    def key_word(self: Self) -> None:
        found_intents: set[Any] = set()

        for intent, words in self.key_words_map.items():
            for word in words:
                if re.search(rf"\b{re.escape(word)}\b", self.text):
                    found_intents.add(intent)

        # return {
        #     "key_words": list(found_intents)
        # }
        if found_intents:
            self.key_words = list(found_intents)
            self.add_log("key_word_log", color="green", start_time=self.start_time)
        else:
            self.add_log("key_word_not_found_log", color="green", start_time=self.start_time)
