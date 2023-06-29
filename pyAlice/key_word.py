from pyAlice.errors.base_errors import KeyWordsErrors
from pyAlice.base import Base


class KeyWord(Base):
    def __init__(self, text, settings, start_time):
        self.start_time = start_time
        self.settings = settings
        self.key_words = settings.KEY_WORD
        self.text = text
        self.add_log("key_word_init_log", color="green", start_time=self.start_time)

    def key_word(self):
        flag = False
        answer = ""
        answer_buttons = []
        answer_message = ""
        answer_event = ""
        for key, value in self.key_words.items():
            for item in value["key_words"]:
                if item in self.text:
                    if flag:
                        raise KeyWordsErrors("key_word_duplicate_error", language=self.settings.LANGUAGE)
                    answer = key
                    answer_buttons = value["buttons"]
                    answer_message = value["message"]
                    answer_event = value["event"]
                    flag = True
        if not flag:
            return False
        return {
            "key_word": answer,
            "event": answer_event,
            "message": answer_message,
            "buttons": answer_buttons,
        }








if __name__ == "__main__":


    a = KeyWord("../testing/key_word", "привет тебе нужна помощь функции")

    print(a.key_word())



#
