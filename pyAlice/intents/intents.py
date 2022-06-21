import json
import pathlib
import datetime
from pyAlice.functions import open_json_file, other_items_in_list, find_str_in_list, delete_word_from_list, from_str_to_list_with_strip
from pyAlice.base import Base
from pyAlice.intents.date_time import DateTime
from pyAlice.errors.base_errors import IntentsErrors

special_type = ["$DATETIME"]
special_start_words = {
    "$DATETIME": ["через", "без", "в", "завтра", "полдень", "полночь",
                  "час", "часа", "часов", "полчас", "полчаса", "минут", "минуты",
                  "один", "одну", "день", "дни", "дней", "дня", "дню",
                  "год", "года", "годы", "неделя", "недели", "неделю",
                  "январь января", "февраль", "фнвраля", "март", "марта",
                  "апрель", "апреля", "май", "мая", "июнь", "июня", "июль", "июля", "август", "августа",
                  "сентябрь", "сентября", "октябрь", "октября", "ноябрь", "ноября", "декабрь", "декабря"]
}


class Intents(Base):
    answer = {}
    events = []
    buttons = []
    status_special_type = False
    date_time_key = []
    date_time_data = {}

    def __init__(self, settings, intents_file, text, start_time=datetime.datetime.now()):
        self.settings = settings
        try:
            self.intents = open_json_file(intents_file)
            if self.intents == "" or self.intents == {}:
                raise IntentsErrors("intents_file_empty_error")
        except json.decoder.JSONDecodeError as error:
            raise IntentsErrors("intents_file_json_error")

        self.text = text
        self.list_text = [item.strip() for item in text.split(" ")]
        self.start_time = start_time
        self.add_log("init_intents_log", start_time=self.start_time)
        self.status_special_type = self.check_special_type()
        self.__separation_intents()

    def check_special_type(self):
        for item in special_type:
            if item in str(self.intents):
                return True
                break
        return False

    def __separation_intents(self):
        if "$DATETIME" in str(self.intents):
            date_time = DateTime(self.text, self.settings, start=self.start_time)
            if date_time.total_success:
                date_time_in_text = date_time.get_data()
                for key, value in date_time_in_text.items():
                    text = value["text"]
                    date_key = find_str_in_list(self.list_text, text)
                    self.date_time_key.append(date_key)
                    self.date_time_data[date_key] = value.get("time")
        for key, value in self.intents.items():
            result = self.intent(value.get("sections"))
            if result != False:
                self.answer[key] = result
                events = value.get("events")
                self.events.append(events if events is not None else False)
                buttons = value.get("buttons")
                self.buttons.extend(from_str_to_list_with_strip(buttons, ",") if buttons is not None else False)

    def intent(self, intent):
        answer = {}
        start_words = []
        start_words_for_intent = {}
        flag_date_time = False
        name_keys_date_time = []
        required_field = []
        for key, value in intent.items():
            if value.get("mandatory_presence"):
                required_field.append(key)
            if value.get("key_word") == "$DATETIME":
                name_keys_date_time.append(key)
                start_words.extend(special_start_words.get("$DATETIME"))
                start_words_for_intent[key] = special_start_words.get("$DATETIME")
                flag_date_time = True
                continue
            start_words_for_intent[key] = value.get("key_word")
            start_words.extend(value.get("key_word").split(","))
        start_words = [word.strip() for word in start_words]
        write = False
        name_write = ""
        special_write = False
        special_write_content = {}
        i = 0
        for item in self.list_text:
            if flag_date_time:
                # print(f"{item.strip().lower()} -------------------------------> {item.strip().lower() in start_words}")
                if item.strip().lower() in start_words or item.isdigit() or ":" in item:
                    for key, value in start_words_for_intent.items():
                        if key in name_keys_date_time and i in self.date_time_key:
                            write = True
                            name_write = key
                            special_write = True
                            special_write_content = self.date_time_data.get(i)
                            start_words = delete_word_from_list(start_words, value)
                            break
                        if item.strip().lower() in value and key not in name_keys_date_time:
                            special_write = False
                            write = True
                            name_write = key
                            start_words = delete_word_from_list(start_words, value)
                            break
            else:
                # print(f"{item.strip().lower()} -------------------------------> {item.strip().lower() in start_words}")
                if item.strip().lower() in start_words:
                    for key, value in start_words_for_intent.items():
                        if item.strip().lower() in value:
                            write = True
                            name_write = key
                            start_words = delete_word_from_list(start_words, value)
                            break
            if write:
                if special_write:
                    if answer.get(name_write) is None:
                        answer[name_write] = special_write_content
                elif not answer.get(name_write) == None:
                    answer[name_write]["full_value"] += f"{item} "
                    answer[name_write]["value"] += f"{item} " if item not in start_words_for_intent.get(name_write) else ""
                else:
                    answer[name_write] = {"full_value": f"{item} ", "value": f"{item} " if item not in start_words_for_intent.get(name_write) else ""}
            i += 1
        for item in required_field:
            if item not in answer.keys():
                answer = False
                break
        # print(answer, "<------------------ ответ")
        return answer

    def get_intents_data(self):
        return {
            "intents": self.answer,
            "events": self.events,
            "buttons": self.buttons
        }

















if __name__ == '__main__':
    print(pathlib.Path.cwd())
    a = Intents("../testing/intents", "из раменского до выхино в 14:00")
# hello
