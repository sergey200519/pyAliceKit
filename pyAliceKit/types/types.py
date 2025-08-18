from typing import Protocol, Dict, Literal, Optional


class SettingsProtocol(Protocol):
    DEBUG: bool
    LOG_OUTPUT_IMMEDIATELY: bool
    TIME_ZONE: Optional[str]
    EVENTS: bool
    TEXT_FOR_KEY_WORDS: Literal["command", "original_utterance"]
    VERSION: str
    ALL_MESSAGES: Dict[str, str]
    STARTING_MESSAGE: str
    ERROR_MESSAGE: str
    HELP_MESSAGE: str
    DEBUG_LANGUAGE: str
    LANGUAGE: str
    SOURCE_TEXT: Literal["command", "original_utterance"]

