import json
from module.errors import KeyWordError


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

        key_word_answer = ""
        events = ""
        dialogs = ""
        buttons = []

        for key, value in key_word_dict.items():
            key_word_list = value["key_word"].split(",")
            for item in key_word_list:
                if item.strip() in self.text:
                    key_word_answer += key + " "
                    events = value["event"]
                    dialogs = value["dialog"]
                    buttons.extend(value["buttons"].split(","))
                    break
        if key_word_answer == "":
            return False
        key_word_answer = key_word_answer[:-1] if key_word_answer[-1] == " " else key_word_answer
        if len(key_word_answer.split(" ")) > 1:
            return {
                "key_word": key_word_answer,
                "event": events,
                "dialog": dialogs,
                "buttons": buttons,
                "success": False
            }
        else:
            if len(key_word_answer.split(" ")) < 1:
                return False
            return {
                "key_word": key_word_answer,
                "event": events,
                "dialog": dialogs,
                "buttons": buttons,
                "success": True
            }








if __name__ == "__main__":


    a = KeyWord("../testing/key_word", "привет тебе нужна помощь функции")

    print(a.key_word())



#
