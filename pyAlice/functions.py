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
    if new_settings.get("events") and type(new_settings.get("events")) != bool:
        return "events_setting_log_error"
    if new_settings.get("debug") and type(new_settings.get("debug")) != bool:
        return "debug_setting_log_error"
    if new_settings.get("buttons_dialogs_auto") and type(new_settings.get("buttons_dialogs_auto")) != bool:
        return "buttons_dialogs_auto_setting_log_error"
    if new_settings.get("time_zone") and (new_settings.get("time_zone") == "" or len(new_settings.get("time_zone")) > 5):
        return "time_zone_setting_log_error"
    # слелать проверку now
    if new_settings.get("text_for_intents") and (new_settings.get("text_for_intents") != "commands" or new_settings.get("text_for_intents") != "original_utterance"):
        return "text_for_intents_text_for_key_word_setting_log_error"
    if new_settings.get("text_for_key_word") and (new_settings.get("text_for_key_word") != "commands" or new_settings.get("text_for_intents") != "original_utterance"):
        return "text_for_intents_text_for_key_word_setting_log_error"
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




















#
