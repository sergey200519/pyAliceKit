# pyAliceKit

**Фреймворк Python для создания диалоговых ботов в Яндекс.Диалоги.**

Версия: 0.1.0

---

## 🚀 Установка

Установка напрямую с GitHub:

```bash
pip install git+https://github.com/sergey200519/pyAliceKit.git@develop
```

Python >= 3.10

---

## 📦 Структура пакета

- `pyAliceKit/` — основной пакет
  - `py_alice/` — ядро диалогового движка
  - `core/` — кнопки, ключевые слова, интенты, сессии
  - `utils/` — вспомогательные функции (dialogs, validation, tools)
  - `GUI/` — визуализация диалогов (Flask + HTML/JS)
- `testing/` — пример настроек и диалогов

---

## ⚡ Простой пример

```python
from pyAliceKit.py_alice.py_alice import PyAlice
from testing import settings

# Пример события от пользователя
event = {"request": {"original_utterance": "привет"}}

# Инициализация бота
alice = PyAlice(params_alice=event, settings=settings)

# Получение ответа
response = alice.get_response_for_alice(type="dict")
print(response)
```

---

## 📖 Пример диалога (ветвящаяся история)

```python
from pyAliceKit.utils.dialogs import include_nodes
from testing.settings import DIALOG_NODES

# Включение диалогов с дочерними узлами
start_story = DIALOG_NODES["start_story"]

# Навигация по левому пути
left_path = start_story["childs"]["left"]
print(left_path["message"])  # start_left_message
```

---

## 🎮 Пример игры без сохранения

```python
DIALOG_NODES["guess_game"] = {
    "message": "Я загадал число от 1 до 10. Попробуй угадать!",
    "buttons": [],
    "events": ["start_guess_game"],
    "meta": {"desc": "Мини-игра угадай число"}
}
```

Событие `start_guess_game` генерирует случайное число и проверяет ввод пользователя.
```python
@on_event("start_guess_game")
def test_event(event: dict[str, Any], *args: Any, **kwargs: Any) -> None:
    pass
```

---


## 🌐 Запуск Flask API для Алисы

```python
from flask import Flask, request, jsonify
from pyAliceKit.py_alice.py_alice import PyAlice
from testing import settings

app = Flask(__name__)

@app.route("/", methods=["POST"])
def alice_handler():
    event = request.get_json()
    pyAlice = PyAlice(params_alice=event, settings=settings)
    response = pyAlice.get_response_for_alice(type="dict")
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)
```

---

## 🔧 Полезные функции

- `include_nodes(nodes_dict, recursive=True)` — подключает дочерние узлы.

---

## 📄 Лицензия

MIT License. См. [LICENSE](LICENSE).

---

## 📝 TODO (v0.1+)

- Полная валидация DIALOG\_NODES
- Тесты `pytest`
- Расширение GUI для редактирования узлов
- Примеры API с запросами к внешним сервисам
