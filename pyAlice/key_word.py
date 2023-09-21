from pyAlice.errors.errors import KeyWordsErrors
from pyAlice.base import Base


class KeyWord(Base):
    def __init__(self, text, settings, start_time):
        self.start_time = start_time
        self.settings = settings
        self.key_words = settings.KEY_WORD
        self.text = text
        self.add_log("key_word_init_log", color="green", start_time=self.start_time)

    def key_word(self):
        answer = []
        answer_buttons = []
        answer_messages = []
        answer_events = []
        for key, value in self.key_words.items():
            for item in value["key_words"]:
                if item in self.text:
                    answer.append(key)
                    answer_buttons.extend(value["buttons"])
                    answer_messages.append(value["message"])
                    answer_events.append(value["event"])
        return {
            "key_words": answer,
            "events": answer_events,
            "messages": answer_messages,
            "buttons": answer_buttons,
        }








if __name__ == "__main__":


    a = KeyWord("../testing/key_word", "привет тебе нужна помощь функции")

    print(a.key_word())