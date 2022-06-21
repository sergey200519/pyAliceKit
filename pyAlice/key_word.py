import json
from pyAlice.errors.base_errors import KeyWordsErrors


class KeyWord:
    def __init__(self, key_words_file, text, dir):
        self.key_words_file = key_words_file
        self.text = text
        self.dir = dir

    def name_file_validate(self, name):
        if ".json" in name:
            return name
        else:
            return f"{name.strip()}.json"

    def key_word(self):
        with open(self.name_file_validate(f"{self.dir}/{self.key_words_file}"), "r") as f:
            key_word_dict = json.loads(f.read())

        answer = ""
        answer_buttons = []
        answer_dialog = ""
        answer_events = []
        for key, value in key_word_dict.items():
            word_from_json = value["key_words"]
            if word_from_json.isspace() or word_from_json == "":
                raise KeyWordsErrors("key_wods_empty_error")
            for item in word_from_json.split(","):
                if item.strip() in self.text:
                    answer += f"{key} "
                    if value.get("events"):
                        for item in value.get("events").split(","):
                            answer_events.append(item.strip())
                    if value.get("buttons"):
                        for item in value.get("buttons").split(","):
                            answer_buttons.append(item.strip())
                    if value.get("dialog"):
                        answer_dialog = value["dialog"]
        if answer == "":
            return False
        answer = answer.strip()
        if len(answer.split(" ")) > 1:
            return {
                "key_word": answer,
                "event": answer_events,
                "dialog": answer_dialog,
                "buttons": answer_buttons,
                "success": False
            }
        else:
            return {
                "key_word": answer,
                "event": answer_events,
                "dialog": answer_dialog,
                "buttons": answer_buttons,
                "success": True
            }








if __name__ == "__main__":


    a = KeyWord("../testing/key_word", "привет тебе нужна помощь функции")

    print(a.key_word())



#
