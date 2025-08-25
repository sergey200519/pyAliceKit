import inspect
import os
import json
from typing import Any, Union
from testing.test2 import insertion


DEBUG = True

def include_nodes(obj: dict[str, Any], DEBUG: bool) -> dict[str, Any]:
    if not DEBUG:
        return obj

    frame_info = inspect.stack()[1]
    frame = frame_info.frame
    filename = frame.f_globals.get("__file__", None)

    import_name = None
    for name, val in frame.f_globals.items():
        if val is obj:
            import_name = name
            break

    # Определяем уровень вложенности
    def get_depth(o: Any, level=1) -> int:
        if isinstance(o, dict):
            for v in o.values():
                if isinstance(v, dict) and "__source__" in v:
                    return get_depth(v["__value__"], level + 1)
        return level

    depth = get_depth(obj)

    return {
        "__value__": obj,
        "__source__": {
            "parent": filename,
            "depth": depth,
            "dependencies": {
                filename: {
                    "import_name": import_name,
                    "value": obj,
                    "depth": depth
                }
            }
        }
    }


test_dict = {
    "key": "value",
    "ins": {
        "key2": include_nodes(insertion, DEBUG)
    }
}

from typing import Any, Union

def get_with_sources(element: Union[dict[Any, Any], list[Any]]) -> dict[str, Any]:
    def unwrap(obj):
        if isinstance(obj, dict) and '__value__' in obj and '__source__' in obj:
            sources.append(obj['__source__'])
            return unwrap(obj['__value__'])
        elif isinstance(obj, dict):
            return {k: unwrap(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [unwrap(i) for i in obj]
        return obj

    def clean(obj):
        if isinstance(obj, dict):
            if "__value__" in obj and "__source__" in obj:
                return clean(obj["__value__"])
            return {k: clean(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean(v) for v in obj]
        return obj

    sources = []
    unwrapped = unwrap(element)

    merged_sources = {
        "parent": sources[0]["parent"] if sources else None,
        "dependencies": {}
    }

    max_depth = 1
    depth_map: dict[int, list[dict[str, Any]]] = {}

    for src in sources:
        for path, dep in src["dependencies"].items():
            cleaned_value = clean(dep["value"])
            depth = dep.get("depth", 1)
            max_depth = max(max_depth, depth)

            # Добавляем в общую зависимость
            merged_sources["dependencies"][path] = {
                "import_name": dep["import_name"],
                "value": cleaned_value,
                "depth": depth
            }

            # Добавляем в карту глубин
            depth_map.setdefault(depth, []).append({
                "path": path,
                "import_name": dep["import_name"],
                "value": cleaned_value
            })

    return {
        "value": unwrapped,
        "sources": merged_sources,
        "max_depth": max_depth,
        "depth_map": depth_map
    }





print(json.dumps(test_dict, ensure_ascii=False))
print(json.dumps(get_with_sources(test_dict), ensure_ascii=False))



# итоговый  вывод:
# {
#     "value": {
#         'key': 'value',
#         'ins': {
#             'key2': {
#                 'key-i': 'value'
#             }
#         }
#     },
#     "sources": {
#         "parent": "/home/sergey/Рабочий стол/python/pyAliceKit/testing/test.py",
#         "dependencies": {
#             "/home/sergey/Рабочий стол/python/pyAliceKit/testing/test.py": {
#                 "import_name": "insertion",
#                 "value": {
#                     "key-i": "value"
#                 }
#             }
#         }
#     }
# }













{
    'stop': {
        'message': 'end_message',
        'buttons': ['$start_buttons'], 
        'events': ['on_stop'], 
        'meta': {
            'desc': 'Выход из диалога.', 
            'version': '1.0'
            }
        }, 
        'help': {
            'message': 'help', 
            'buttons': ['$main_buttons'], 
            'events': ['on_help'], 'keywords': ['help'], 
            'meta': {'desc': 'Справка по доступным командам.', 'version': '1.0'}
        }, 
        'start_story': {
            'message': 'start_story_message',
            'buttons': ['$left'],
            'events': ['on_start_story'],
            'keywords': ['start'],
            'image': 'img1',
            'childs': {
                'left': {
                    '__value__': {
                        'message': 'start_left_message', 'buttons': ['$fight_or_run'], 'events': [], 'keywords': ['left'], 'childs': {'end': {'message': 'left_end_message', 'buttons': [], 'events': ['on_end'], 'transitions': ['$prev'], 'meta': {'desc': 'Конец левой ветки.', 'version': '1.0'}, 'end_dialog': True}}, 'transitions': ['/help'], 'meta': {'desc': 'Левая ветка истории: лес и волк.', 'version': '1.0'}}, '__source__': {'parent': '/home/sergey/Рабочий стол/python/pyAliceKit/testing/left_story.py', 'depth': 1, 'dependencies': {'/home/sergey/Рабочий стол/python/pyAliceKit/testing/left_story.py': {'import_name': None, 'value': {'message': 'start_left_message', 'buttons': ['$fight_or_run'], 'events': [], 'keywords': ['left'], 'childs': {'end': {'message': 'left_end_message', 'buttons': [], 'events': ['on_end'], 'transitions': ['$prev'], 'meta': {'desc': 'Конец левой ветки.', 'version': '1.0'}, 'end_dialog': True}}, 'transitions': ['/help'], 'meta': {'desc': 'Левая ветка истории: лес и волк.', 'version': '1.0'}}, 'depth': 1}}}}, 'right': {'__value__': {'message': 'start_right_message', 'buttons': ['$right'], 'events': [], 'keywords': ['right'], 'childs': {'talk': {'message': 'right_talk_message', 'buttons': [], 'events': ['on_end'], 'transitions': ['$prev'], 'meta': {'desc': 'Диалог с человеком в городе.', 'version': '1.0'}}, 'hide': {'message': 'right_hide_message', 'buttons': [], 'events': ['on_end'], 'transitions': ['$prev'], 'meta': {'desc': 'Ты спрятался в переулке.', 'version': '1.0'}}}, 'chooser': <function choose_right_path at 0x7223990ec360>, 'transitions': ['/help', '$prev'], 'meta': {'desc': 'Правая ветка истории: город и человек.', 'version': '1.0'}}, '__source__': {'parent': '/home/sergey/Рабочий стол/python/pyAliceKit/testing/right_story.py', 'depth': 1, 'dependencies': {'/home/sergey/Рабочий стол/python/pyAliceKit/testing/right_story.py': {'import_name': None, 'value': {'message': 'start_right_message', 'buttons': ['$right'], 'events': [], 'keywords': ['right'], 'childs': {'talk': {'message': 'right_talk_message', 'buttons': [], 'events': ['on_end'], 'transitions': ['$prev'], 'meta': {'desc': 'Диалог с человеком в городе.', 'version': '1.0'}}, 'hide': {'message': 'right_hide_message', 'buttons': [], 'events': ['on_end'], 'transitions': ['$prev'], 'meta': {'desc': 'Ты спрятался в переулке.', 'version': '1.0'}}}, 'chooser': <function choose_right_path at 0x7223990ec360>, 'transitions': ['/help', '$prev'], 'meta': {'desc': 'Правая ветка истории: город и человек.', 'version': '1.0'}}, 'depth': 1}}}}}, 'transitions': ['/help', '$prev'], 'meta': {'desc': 'Начало истории. Выбор направления.', 'version': '1.0'}}}