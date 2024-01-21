import datetime, json
from pyAlice.errors.errors import SettingsErrors, StorageErrors, MessageErrors

from pyAlice.messages.embedded_message import embedded_message


class Base:
    # bool
    new, end_session, inaction = False, False, True
    # str
    result_message, came_message = "", ""
    # dict
    intents, storage, events, logs, more_data_message = {}, {}, {}, {}, {}
    # list
    buttons, alice_buttons, key_words = [], [], []

    EMBEDDED_MESSAGE = embedded_message

    
    