import json
import os
from types import ModuleType
from typing import Any, Optional, Self

from pyAliceKit.utils.dialogs import flatten_dialogs
from pyAliceKit.utils.errors.errors import DialogEngineErrors


class DialogEngine:
    def __init__(self: Self, settings: ModuleType, pyAlice: "PyAlice") -> None: # type: ignore
        self.__settings: ModuleType = settings
        self.__pyAlice: "PyAlice" = pyAlice # type: ignore
        self.__dialogs_map_file: str = self.__settings.DIALOGS_MAP_FILE
        self.dialog: Optional[str] = None  # Текущий диалог, если он найден

        # Плоская карта диалогов
        self.__dialogs_map: dict[str, dict[str, Any]] = {}

        self.__init_dialogs_map()

    def __init_dialogs_map(self: Self) -> None:
        try:
            if os.path.exists(self.__dialogs_map_file):
                with open(self.__dialogs_map_file, "r", encoding="utf-8") as f:
                    self.__dialogs_map = json.load(f)
            if self.__settings.DEBUG:
                dialogs = getattr(self.__settings, "DIALOGS", {})
                self.__dialogs_map = flatten_dialogs(dialogs)
                with open(self.__dialogs_map_file, "w", encoding="utf-8") as f:
                    json.dump(self.__dialogs_map, f, ensure_ascii=False, indent=4)
            else:
                raise DialogEngineErrors("dialog_map_file_not_found", language=self.__settings.DEBUG_LANGUAGE)
        except Exception as e:
            raise DialogEngineErrors("dialog_map_load_failed", context=str(e), language=self.__settings.DEBUG_LANGUAGE)

    def find_best_dialog(self: Self) -> Optional[str]:
        scores: dict[str, int] = {}

        came_message = self.__pyAlice.came_message.lower()
        seen_events = set(self.__pyAlice.events.get_events())
        key_words = set(self.__pyAlice.key_words.key_words)
        intent_names = set(self.__pyAlice.intents.get_intent_names())
        previous = self.__pyAlice.previous_dialogue

        # Определяем множество кандидатов для сужения поиска
        allowed_dialogs = set()

        # 1) Глобальные (корневые) диалоги — с одним уровнем '/'
        allowed_dialogs.update([
            name for name in self.__dialogs_map
            if name.count("/") == 1
        ])

        # 2) Первые потомки предыдущего диалога
        if previous and previous in self.__dialogs_map:
            previous_data = self.__dialogs_map[previous]
            allowed_dialogs.update(previous_data.get("childs", []))

            # 3) Диалоги из переходов предыдущего
            transitions = previous_data.get("transitions", {})
            # Если в ключевых словах есть "prev" — то разрешаем переход по "$prev" (заменяем его на previous)
            for target in transitions.values():
                if target == "$prev" and "prev" in key_words:
                    allowed_dialogs.add(previous)
                else:
                    allowed_dialogs.add(target)

        # Если нет previous, ищем среди всех (можно ограничить и здесь, если нужно)
        if not previous:
            allowed_dialogs = set(self.__dialogs_map.keys())

        for dialog_name, dialog_data in self.__dialogs_map.items():
            # Сужаем поиск до allowed_dialogs, если previous есть
            if previous and dialog_name not in allowed_dialogs:
                continue

            score = 0
            reasons = []

            # События
            dialog_events = set(dialog_data.get("events", []))
            matched_events = dialog_events & seen_events
            if matched_events:
                score += len(matched_events)
                reasons.append("matched_events")

            # Ключевые слова
            dialog_keywords = set(dialog_data.get("keywords", []))
            matched_keywords = dialog_keywords & key_words
            if matched_keywords:
                score += len(matched_keywords) * 2
                reasons.append("matched_keywords")

            # Интенты
            matched_intents = intent_names & set(dialog_data.get("intents", []))
            if matched_intents:
                score += len(matched_intents) * 2
                reasons.append("matched_intents")

            # Переходы от предыдущего
            if previous and previous in self.__dialogs_map:
                transitions = self.__dialogs_map[previous].get("transitions", {})
                for trigger in key_words | intent_names:
                    target_dialog = transitions.get(trigger)
                    # Приоритетно обрабатываем $prev если "prev" в ключевых словах
                    if target_dialog == "$prev" and "prev" in key_words:
                        target_dialog = previous
                    if target_dialog == dialog_name:
                        score += 3
                        reasons.append("matched_transition")
                        break

            # Частичное совпадение по сообщению
            message_text = dialog_data.get("message", "").lower()
            if message_text and message_text in came_message:
                score += 1
                reasons.append("matched_message")

            # Приоритет из meta
            priority = dialog_data.get("meta", {}).get("priority", 0)
            if isinstance(priority, int) and priority > 0:
                score += priority
                reasons.append("meta_priority")

            if score > 0:
                scores[dialog_name] = score
                self.__pyAlice.add_log(
                    "dialog_score_log",
                    color="yellow",
                    context=f"{dialog_name}: {score} ({', '.join(reasons)})",
                    start_time=self.__pyAlice.start_time
                )

        result = max(scores, key=scores.get) if scores else None
        self.dialog = result

        if result:
            self.__pyAlice.add_log(
                "dialog_selected_log",
                color="green",
                context=result,
                start_time=self.__pyAlice.start_time
            )
        else:
            self.__pyAlice.add_log(
                "dialog_not_found_log",
                color="red",
                start_time=self.__pyAlice.start_time
            )

        return result





    def get_dialog(self: Self, name: str) -> Optional[dict[str, Any]]:
        return self.__dialogs_map.get(name)

    def get_all(self: Self) -> dict[str, dict[str, Any]]:
        return self.__dialogs_map