import datetime
from pyAlice.base import Base
from pyAlice.functions import slice_list
from dateutil.relativedelta import relativedelta


words_signal = ["через", "без", "в", "завтра", "полдень", "полночь",
                "час", "часа", "часов", "полчас", "полчаса", "минут", "минуты",
                "один", "одну", "день", "дни", "дней", "дня", "дню",
                "год", "года", "годы", "неделя", "недели", "неделю"]
months = {
    "январь января": "01",
    "февраль фнвраля": "02",
    "март марта": "03",
    "апрель апреля": "04",
    "май мая": "05",
    "июнь июня": "06",
    "июль июля": "07",
    "август августа": "08",
    "сентябрь сентября": "09",
    "октябрь октября": "10",
    "ноябрь ноября": "11",
    "декабрь декабря": "12"
}


class DateTime(Base):
    total_answer = {}
    success = False
    total_success = True

    def __init__(self, string, settings, now=datetime.datetime.now(), start_time=datetime.datetime.now()):
        self.string = string
        self.start_time = start_time
        self.now = now
        self.settings = settings
        self.add_log("init_datetime_log", start_time=self.start_time)
        self.search()
        if self.total_answer:
            self.add_log("finish_datetime_log", start_time=self.start_time, correction=f"Время распознавания {str(datetime.datetime.now()- self.now)[5:]}")
        else:
            self.total_success = False
            self.add_log("finish_datetime_log_error", start_time=self.start_time)

    def search(self):
        self.add_log("search_datetime_log", start_time=self.start_time)
        i = 0
        j = 0
        for item in self.string.split(" "):
            if j > 0:
                j -= 1
                continue
            if (item.lower().strip() in words_signal or ":" in item.lower().strip() or item.strip().isdigit()) and j <= 0:
                if len(item) > 1 and "в" in item:
                    continue
                res = self.__date_time(self.string[self.string.find(item, i):])
                # print(f"res -> {res}, item -> {item}")
                if res["success"]:
                    self.total_answer = {
                        "time": res["value"],
                        "text": res["text"]
                        }
                    if res["word_break"] != "":
                        n_continue_let = self.n_continue(self.string, item, res["word_break"])
                        j = n_continue_let[0]
                        j = j if j != None else 0
                        i += n_continue_let[1]
                    else:
                        break
            i += len(item) + 1

    def __date_time(self, string):
        relative_time = False
        break_status = True
        text = ""
        word_break = ""
        self.success = False
        answer = {
            "years": "",
            "months": "",
            "weeks": "",
            "days": "",
            "hours": "",
            "minutes": "",
            "seconds": ""
        }

        def answer_auto_fill(string, n):
            self.success = True
            if string in "год годы года":
                answer["years"] = n
            elif string in "месяц месяца месяцы":
                answer["months"] = n
            elif string in "неделю недели недель":
                answer["weeks"] = n
            elif string in "день дня дней":
                answer["days"] = n
            elif string in "часа час часы часов":
                answer["hours"] = n
            elif string in "минут минуты мин":
                answer["minutes"] = n
            elif string in "секунду седунды сек":
                answer["seconds"] = n
            else:
                self.success = False
            for key, value in months.items():
                if string in key:
                    answer["months"] = value
                    answer["days"] = n
                    self.success = True
                    break

        regarding = False
        string_list = list(filter(None, [item.lower().strip() for item in string.split(" ")]))
        if "через" in string:
            regarding = True
            relative_time = True
            i = 0
            for item in string_list:
                if item not in words_signal and not item.isdigit() and item not in "и в":
                    word_break = item
                    break_status = False
                    self.add_log("found_regarding_time_log", start_time=self.start_time, correction=text)
                    break
                else:
                    text += item + " "
                    if item == "час":
                        answer["hours"] = 1
                        self.success = True
                    if item.isdigit():
                        answer_auto_fill(string_list[i + 1], item)
                    if item in "один одну":
                        answer_auto_fill(string_list[i + 1], 1)
                    if item in "полчас полчаса":
                        answer["minutes"] = 30
                        self.success = True
                i += 1
            if break_status:
                self.add_log("found_regarding_time_log", start_time=self.start_time, correction=text, type="date_time")
        elif "без" in string:
            regarding = True
            i = 0
            for item in string_list:
                if item not in words_signal and not item.isdigit() and item not in "и в":
                    word_break = item
                    break_status = False
                    self.add_log("found_regarding_time_log", start_time=self.start_time, correction=text, type="date_time")
                    break
                else:
                    if item == "без":
                        if string_list[i + 1].isdigit():
                            if string_list[i + 2] in "минут минуту минуты минута":
                                if string_list[i + 3].isdigit():
                                    text += slice_list(string_list, i, i + 3)
                                    answer["hours"] = int(string_list[i + 3]) - 1
                                    answer["minutes"] = 60 - int(string_list[i + 1])
                                    self.success = True
                                break
                            elif string_list[i + 2].isdigit():
                                text += slice_list(string_list, i, i + 2)
                                answer["hours"] = int(string_list[i + 2]) - 1
                                answer["minutes"] = 60 - int(string_list[i + 1])
                                self.success = True
                i += 1
            if break_status:
                self.add_log("found_regarding_time_log", start_time=self.start_time, correction=text, type="date_time")
        else:
            i = 0
            for item in string_list:
                if item not in words_signal and not item.isdigit() and item not in "и в" and not self.is_month(item) and not ":" in item:
                    word_break = item
                    break_status = False
                    self.add_log("found_time_log", start_time=self.start_time, correction=text)
                    break
                else:
                    text += item + " "
                    if ":" in item and len(item) <= 5:
                        time = self.recognize_time(item)
                        answer["hours"] = time["hours"]
                        answer["minutes"] = time["minutes"]
                        self.success = True
                    if item.isdigit():
                        answer_auto_fill(string_list[i + 1], item)
                    if item in "один одну":
                        answer_auto_fill(string_list[i + 1], 1)
                    if item in "полдень":
                        answer["hours"] = "12"
                        self.success = True
                    if item in "полночь":
                        answer["hours"] = "00"
                        self.success = True
                i += 1
            if break_status:
                self.add_log("found_time_log", start_time=self.start_time, correction=text, type="date_time")
        # print(self.success, answer)
        return {
            "value": self.__colect_answer(answer, relative=relative_time),
            "word_break": word_break,
            "success": self.success,
            "text": text
        }

    def recognize_time(self, string):
        time = string.split(":")
        return {
            "hours": time[0],
            "minutes": time[1]
        }

    def is_month(self, string):
        for key, value in months.items():
            if string.lower().strip() in key:
                return True
        return False

    def n_continue(self, string, this_word, need_word):
        # print(f"{string} - {this_word} - {need_word}")
        i = 0
        j = 0
        status = False
        for item in string.split(" "):
            if item == this_word:
                status = True
            if item == need_word:
                status = False
                return (i, j)
            if status:
                i += 1
                j += len(item)

    def __colect_answer(self, old_answer, relative=False):
        if not relative:
            now = datetime.datetime.now()
            year, month, week, day, hours, minutes, seconds = now.year, now.month, 0, now.day, now.hour, now.minute, now.second
            if old_answer["years"] != "":
                year = int(old_answer["years"])
            if old_answer["months"] != "":
                month = int(old_answer["months"])
            if old_answer["weeks"] != "":
                day + int(old_answer["weeks"]) * 7
            if old_answer["days"] != "":
                day = int(old_answer["days"])
            if old_answer["hours"] != "":
                hours = int(old_answer["hours"])
            if old_answer["minutes"] != "":
                minutes = int(old_answer["minutes"])
            if old_answer["seconds"] != "":
                seconds = int(old_answer["seconds"])
            date_time = datetime.datetime.strptime(f"{year}-{month}-{day} {hours}:{minutes}:{seconds}", '%Y-%m-%d %H:%M:%S')
            return date_time
        elif relative:
            year, month, week, day, hours, minutes, seconds = 0, 0, 0, 0, 0, 0, 0
            if old_answer["years"] != "":
                year = int(old_answer["years"])
            if old_answer["months"] != "":
                month = int(old_answer["months"])
            if old_answer["weeks"] != "":
                week = int(old_answer["weeks"])
            if old_answer["days"] != "":
                day = int(old_answer["days"])
            if old_answer["hours"] != "":
                hours = int(old_answer["hours"])
            if old_answer["minutes"] != "":
                minutes = int(old_answer["minutes"])
            if old_answer["seconds"] != "":
                seconds = int(old_answer["seconds"])
            new_date_time = datetime.datetime.now() + relativedelta(years=year, months=month, weeks=week, hours=hours, minutes=minutes, seconds=seconds)
            return new_date_time
        return False

    def get_data(self):
        self.add_log("get_datetime_log", start_time=self.start_time)
        return self.total_answer
# '_'


if __name__ == '__main__':
    a = "из раменского 27 мая в 14:34 до выхино"
    # a = "привет я буду 27 мая 2020 года в 15:44 дома и в 17:55"
    # a = "привет я пришол в гости в 19:44"
    # a = "я через 2 недели буду   дома"
    # a = "привет и пока"
    b = DateTime(a, settings={"debug": True})
    print(b.total_answer)
    b.get_data()
    print(b.logs())
