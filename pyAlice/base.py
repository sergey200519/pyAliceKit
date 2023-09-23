import datetime, json

from pyAlice.errors.errors import MessageErrors, SettingsErrors, StorageErrors
from pyAlice.messages.embedded_message import embedded_message


class Base:
    # bool
    new = False
    # str
    result_message, text = "", ""
    # dict
    intents, message, storage, events, logs, response, more_data_message = {}, {}, {}, {}, {}, {}, {}
    # list
    buttons, alice_buttons, key_word = [], [], []

    EMBEDDED_MESSAGE = embedded_message


    def add_log(self, log, color=None, context="", start_time=datetime.datetime.now()):
        if not self.settings.DEBUG:
            return
        delta_time = datetime.datetime.now() - start_time

        # time = str(datetime.datetime.now() - start_time)[5:]
        time = f"{delta_time.seconds}s {delta_time.microseconds} micros"
        log_text = self.EMBEDDED_MESSAGE.get(f"{log}-{self.settings.DEBUG_LANGUAGE}").format(context)
        self.logs[time] = f"{log_text}"
        if self.settings.LOG_OUTPUT_IMMEDIATELY:
            colors = {
                "black": "30",
                "red": "31",
                "green": "32",
                "yellow": "33",
                "blue": "34",
                "purple": "35",
                "turquoise": "36",
                "white": "37"
            }
            if color is not None:
                color_str = f"\033[{colors.get(color)}m"
                print(f"{color_str}{time}  -->  {log_text}\033[0m")
            else:
                print(f"{time}  -->  {log_text}")
    def get_message(self, message):
        answer = self.settings.ALL_MESSAGES.get(message)
        if answer is None:
            raise MessageErrors("dialog_not_found_error", context=message, language=self.settings.DEBUG_LANGUAGE)
        return answer
    
    def get_buttons_name(self):
        answer = []
        for item in self.buttons:
            if "$" in item:
                grop_buttons = self.settings.BUTTONS_GROUPS.get(item)
                if grop_buttons is None:
                    raise SettingsErrors("group_buttons_not_found_error", context=item, language=self.settings.DEBUG_LANGUAGE)
                for it in grop_buttons:
                    answer.append(it)
            else:
                answer.append(item)
        return answer

    def get_buttons(self):
        answer = []
        for item in self.get_buttons_name():
            button = self.settings.BUTTONS.get(item)
            if button is None:
                raise SettingsErrors("button_not_found_error", context=item, language=self.settings.DEBUG_LANGUAGE)
            if button not in answer:
                answer.append(button)
        self.add_log("buttons_success_founded", color="yellow", start_time=self.start_time)
        return answer
    
    def add_button(self, name):
        if name not in self.buttons:
            self.buttons.append(name)
            self.alice_buttons = self.get_buttons()
    
    def add_buttons(self, buttons):
        for item in buttons:
            self.add_button(item)
    
    def get_storage(self):
        return self.storage
    
    def get_storage_by_key(self, key):
        data = self.storage.get(key)
        if data is None:
            raise StorageErrors("item_in_storage_not_found_error", context=key, language=self.settings.DEBUG_LANGUAGE)
        return data
    
    def set_storage(self, key, data, overwrite=True):
        if key in self.storage.keys() and not overwrite:
            raise StorageErrors("overwrite_storage_error", context=key, language=self.settings.DEBUG_LANGUAGE)
        self.storage[key] = data
    
    def update_storage_by_key(self, key, data):
        if key not in self.storage.keys():
            raise StorageErrors("item_in_storage_not_found_error", context=key, language=self.settings.DEBUG_LANGUAGE)
        self.storage[key] = data
    
    def add_event(self, event, where):
        event_name = event["event"]
        if event_name != "$NULL":
            event_data = {
                "where": where,
                "when": str(datetime.datetime.now() - self.start_time)[5:],
                # "reason": self.__get_reasons("from_key_words_event_resons")
            }
            self.events[event_name] = event_data
            self.add_log("event_success_add", color="blue", context=event_name, start_time=self.start_time)

            fun = self.settings.EVENTS_LIST.get(event_name)
            if fun is not None:
                event["event_data"] = event_data
                fun(event, self)
                self.add_log("event_success_call", color="blue", context=event_name, start_time=self.start_time)
    
    def is_empty_events(self):
        if self.events == {}:
            return True
        for event in self.events.keys():
            if event not in self.settings.IGNORE_EVENTS_LIST:
                return False
        return True
    
    def add_message(self, message_name):
        self.result_message = self.get_message(message_name)
        more_data = self.settings.MORE_DATA_MESSAGES.get(message_name)
        if more_data is not None:
            self.more_data_message = json.loads(json.dumps(more_data).replace("$MESSAGE", self.result_message))
        else:
            self.more_data_message = {}