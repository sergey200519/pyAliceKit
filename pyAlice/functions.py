import pathlib
import json


MAIN_DIR = pathlib.Path.cwd()


def open_json_file(name_file):
    answer = ""
    if ".json" in name_file:
        with open(f"{MAIN_DIR}/{name_file}", "r") as f:
            answer = json.loads(f.read())
    else:
        with open(f"{MAIN_DIR}/{name_file}.json", "r") as f:
            answer = json.loads(f.read())
    return answer


def new_settings_is_valid(new_settings):
    new_settings = open_json_file(new_settings)
    keys = ["events", "debug", "buttons_dialogs_auto", "time_zone",
            "text_for_intents", "text_for_key_words", "version",
            "error_dialog", "dialogs_file", "intents_file", "key_words_file",
            "buttons_file", "const_buttons", "language"]
    for key, value in new_settings.items():
        if key not in keys:
            return "find_unclear_setting_error"
    if new_settings.get("events") and type(new_settings.get("events")) != bool:
        return "events_setting_error"
    if new_settings.get("debug") and type(new_settings.get("debug")) != bool:
        return "debug_setting_error"
    if new_settings.get("buttons_dialogs_auto") and type(new_settings.get("buttons_dialogs_auto")) != bool:
        return "buttons_dialogs_auto_setting_error"
    if new_settings.get("time_zone") and (new_settings.get("time_zone") == "" or len(new_settings.get("time_zone")) > 5):
        return "time_zone_setting_error"
    # слелать проверку now
    if new_settings.get("text_for_intents") and (new_settings.get("text_for_intents") != "commands" or new_settings.get("text_for_intents") != "original_utterance"):
        return "text_for_intents_text_for_key_word_setting_error"
    if new_settings.get("text_for_key_words") and (new_settings.get("text_for_key_word") != "commands" or new_settings.get("text_for_intents") != "original_utterance"):
        return "text_for_intents_text_for_key_word_setting_error"
    if new_settings.get("language") and len(new_settings.get("language")) < 2:
        return "language_setting_error"
    return True


def distribution_of_settings(settings, new_settings):
    for key, value in settings.items():
        if new_settings.get(key):
            settings[key] = new_settings.get(key)
    return settings


def get_buttons(buttons, buttons_file):
    buttons_dict = open_json_file(buttons_file)
    answer = []
    for item in buttons:
        if buttons_dict.get(item.strip()) == None:
            return False
        answer.append(buttons_dict.get(item.strip()))
    return answer


def other_items_in_list(item, lis):
    answer = []
    for it in lis:
        if item != it:
            answer.append(it)
    return answer


def slice_list(list_text, start, end):
    answer = ""
    i = 0
    while i < len(list_text):
        if i >= start and i <= end:
            answer += list_text[i] + " "
        i += 1
    return answer.strip()


def find_str_in_list(list_text, text):
    n = len(text.split(" "))
    text = " ".join(text.split()).split(' ')
    i = 0
    while i < len(list_text):
        if list_text[i:i+n] == text:
            return i
        i += 1
    return -1


def delete_word_from_list(list, words):
    return [word for word in list if word.strip().lower() not in words]


def from_str_to_list_with_strip(text, sign):
    answer = []
    for item in text.split(sign):
        answer.append(item.strip())
    return answer











#
