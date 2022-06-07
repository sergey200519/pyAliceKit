import json
import pathlib
from module.functions import open_json_file, other_items_in_list
from module.base import Base
# from functions import open_json_file, other_items_in_list
import datetime

class Intents(Base):
    answer = {}
    events = []
    status_other_type = False

    def __init__(self, intents_file, text, start_time=datetime.datetime.now()):
        self.intents = open_json_file(intents_file)
        self.text = text
        self.start_time = start_time
        self.add_log("init_intents_log", start_time=self.start_time)


















if __name__ == '__main__':
    print(pathlib.Path.cwd())
    a = Intents("../testing/intents", "из раменского до выхино в 14:00")
# hello
