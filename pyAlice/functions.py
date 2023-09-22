def new_settings_is_valid(new_settings):
    if type(new_settings.EVENTS) != bool:
        return "events_setting_error"
    if type(new_settings.DEBUG) != bool:
        return "debug_setting_error"
    # if type(new_settings.BUTTONS_MESSAGE) != bool:
    #     return "buttons_dialogs_auto_setting_error"
    # if (new_settings.TIME_ZONE == "" or len(new_settings.TIME_ZONE) > 5):
    #     return "time_zone_setting_error"
    # слелать проверку now
    if new_settings.TEXT_FOR_KEY_WORDS != "command" and new_settings.TEXT_FOR_KEY_WORDS != "original_utterance":
        return "text_for_key_word_setting_error"
    if len(new_settings.LANGUAGE) < 2:
        return "language_setting_error"
    if new_settings.STARTING_MESSAGE is None:
        return "starting_dialog_setting_error"
    if new_settings.SOURCE_TEXT is None and (new_settings.SOURCE_TEXT != "commands" or new_settings.SOURCE_TEXT != "original_utterance"):
        return "source_text_setting_error"
    return "success"


def end_alice_event(event, cls):
    cls.end_session_alice()