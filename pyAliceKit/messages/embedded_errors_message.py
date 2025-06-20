embedded_errors_message: dict[str, str] = {
    # Ошибки отсутствия обязательных атрибутов
    "debug_not_set-ru": "Настройка DEBUG не установлена",
    "log_output_immediately_not_set-ru": "Настройка LOG_OUTPUT_IMMEDIATELY не установлена",
    "time_zone_not_set-ru": "Настройка TIME_ZONE не установлена",
    "events_not_set-ru": "Настройка EVENTS не установлена",
    "text_for_key_words_not_set-ru": "Настройка TEXT_FOR_KEY_WORDS не установлена",
    "version_not_set-ru": "Настройка VERSION не установлена",
    "all_messages_not_set-ru": "Настройка ALL_MESSAGES не установлена",
    "starting_message_not_set-ru": "Настройка STARTING_MESSAGE не установлена",
    "error_message_not_set-ru": "Настройка ERROR_MESSAGE не установлена",
    "help_message_not_set-ru": "Настройка HELP_MESSAGE не установлена",
    "debug_language_not_set-ru": "Настройка DEBUG_LANGUAGE не установлена",
    "language_not_set-ru": "Настройка LANGUAGE не установлена",
    "source_text_not_set-ru": "Настройка SOURCE_TEXT не установлена",
    
    # Ошибки типов и значений
    "debug_setting_error-ru": "Настройка DEBUG должна быть булевым значением (True/False)",
    "log_output_immediately_setting_error-ru": "Настройка LOG_OUTPUT_IMMEDIATELY должна быть булевым значением (True/False)",
    "timezone_setting_error-ru": "Настройка TIME_ZONE должна быть строкой или None",
    "events_setting_error-ru": "Настройка EVENTS должна быть булевым значением (True/False)",
    "text_for_key_word_setting_error-ru": "Настройка TEXT_FOR_KEY_WORDS должна быть 'command' или 'original_utterance'",
    "version_setting_error-ru": "Настройка VERSION должна быть строкой",
    "all_messages_setting_error-ru": "Настройка ALL_MESSAGES должна быть словарем",
    "starting_message_setting_error-ru": "STARTING_MESSAGE должен быть непустой строкой и присутствовать в ALL_MESSAGES",
    "error_message_setting_error-ru": "ERROR_MESSAGE должен быть непустой строкой и присутствовать в ALL_MESSAGES",
    "help_message_setting_error-ru": "HELP_MESSAGE должен быть непустой строкой и присутствовать в ALL_MESSAGES",
    "debug_language_setting_error-ru": "Настройка DEBUG_LANGUAGE должна быть строкой",
    "language_setting_error-ru": "Настройка LANGUAGE должна быть строкой",
    "source_text_setting_error-ru": "Настройка SOURCE_TEXT должна быть 'command' или 'original_utterance'",
    
    # Ошибки с кнопками
    "group_buttons_not_found_error-ru": "Группа кнопок '{}' не найдена",
    "button_not_found_error-ru": "Кнопока '{}' не найдена",

    # Ошибки с хранилищем
    "item_in_storage_not_found_error-ru": "Запись в хранилище с именем '{}' не найдена",

    # Ошибки с alice_params
    "new_boolean_setting_error-ru": "Произошла ошибка при поппытке определение 'new'",

    "duplicate_keyword-ru": "Обнаружено дублирование ключевого слова: {}",

    "intent_not_found-ru": "Интент '{}' не найден.",
    "slots_not_found-ru": "У интента '{}' отсутствуют слоты.",
    "slot_not_found-ru": "Слот '{}' не найден.",
    "slot_value_not_found-ru": "У слота '{}' отсутствует значение.",
}