import datetime
from pyAlice.base import Base


words_signal = ["через", "без", "в", "завтра", "полдень", "полночь",
                "час", "часа", "часов", "полчас", "полчаса", "минут", "минуты",
                "один", "одну", "день", "дни", "дней", "дня", "дню",
                "год", "года", "годы", "неделя", "недели", "неделю"]

relative_word = ["через", "без"]

date_time_word = ["завтра", "полдень", "полночь", "час", "часа", "часов",
                  "полчас", "полчаса", "минут", "минуты",
                  "день", "дни", "дней", "дня", "дню",
                  "год", "года", "годы", "неделя", "недели", "неделю",
                  "январь", "января", "февраль", "фнвраля", "март", "марта",
                  "апрель", "апреля", "ноябрь", "ноября"]

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
    def __init__(self, string, settings, now=datetime.datetime.now(), start_time=datetime.datetime.now().time()):
        self.string = string
        self.settings = settings
        self.now = now
        self.start_time = start_time
        self.result = {}
        self.count_result = 0

    def __is_signal(self, word):
        if ":" in word and word.replace(":", "").isdigit():
            return True
        elif word in words_signal or word.isdigit():
            return True
        else:
            return False

    def search(self):
        list_string = self.string.split(" ")
        flag = False
        i = 0
        while i < len(list_string):
            word = list_string[i]
            if self.__is_signal(word):
                if word in relative_word:
                    print(f"rel {word}")
                elif ":" in word and word.replace(":", "").isdigit():
                    time = word.split(":")
                    self.result[self.count_result] = {
                        "date_time": self.create_date_time(hour=time[0], minute=time[1]),
                        "text": word
                    }
                elif word.isdigit():
                    j = i
                    answer = {
                        "years": "",
                        "months": "",
                        "weeks": "",
                        "days": "",
                        "hours": "",
                        "minutes": "",
                        "seconds": ""
                    }
                    while True:
                        if j + 1 == len(list_string):
                            break
                        if list_string[j].isdigit() and list_string[j + 1] in date_time_word:
                            if list_string[j + 1] in "год годы года":
                                answer["years"] = int(list_string[j])
                            elif list_string[j + 1] in "месяц месяца месяцы":
                                answer["months"] = int(list_string[j])
                            elif list_string[j + 1] in "неделю недели недель":
                                answer["weeks"] = int(list_string[j])
                            elif list_string[j + 1] in "день дня дней":
                                answer["days"] = int(list_string[j])
                            elif list_string[j + 1] in "часа час часы часов":
                                answer["hours"] = int(list_string[j])
                            elif list_string[j + 1] in "минут минуты мин":
                                answer["minutes"] = int(list_string[j])
                            elif list_string[j + 1] in "секунду седунды сек":
                                answer["seconds"] = int(list_string[j])
                        if list_string[j] in words_signal:
                            j += 1
                            continue
                        else:
                            break
                        j += 1
                    i = j
                    print(answer)
            i += 1

    def create_date_time(self, year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, second=datetime.datetime.now().second, microsecond=datetime.datetime.now().microsecond):
        print(year, type(year))
        return datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second), microsecond=int(microsecond))


# '_'
