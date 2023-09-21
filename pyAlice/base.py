import datetime


class Base:
    # bool
    new = False
    # str
    default_text, key_word, text = "", "", ""
    # dict
    intents, message, buttons_dict, storage, events, logs = {}, {}, {}, {}, {}, {}
    # list
    buttons = []

