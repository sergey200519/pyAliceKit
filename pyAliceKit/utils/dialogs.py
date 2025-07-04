import inspect
from typing import Any, Callable, TypeVar, cast


# Тип значения узла в диалоге
DialogNode = dict[str, Any]
# Тип функции выбора: принимает строку, возвращает строку
ChooserFunc = Callable[[str], str]
# Обобщённый тип, чтобы не терялась сигнатура оборачиваемой функции
F = TypeVar("F", bound=ChooserFunc)

def chooser(base_url: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def wrapper(user_input: str) -> str:
            leaf = func(user_input)
            return f"{base_url}/{leaf}" if leaf else ""
        return cast(F, wrapper)
    return decorator


def flatten_dialogs(dialogs: dict[str, Any], base_path: str = "") -> dict[str, Any]:
    result: dict[str, Any] = {}

    def walk(node: dict[str, Any], path: str):
        flat_node = {k: v for k, v in node.items() if k != "childs"}

        # Сохраняем исходный код функции chooser, если она есть
        if "chooser" in flat_node and callable(flat_node["chooser"]):
            function_name: str = flat_node["chooser"].__name__
            flat_node["chooser"] = inspect.getsource(flat_node["chooser"]).strip()
            flat_node["chooser_name"] = function_name

        full_path = f"/{path}"
        child_paths = []

        if "childs" in node and isinstance(node["childs"], dict):
            for child_key, child_node in node["childs"].items(): # type: ignore
                child_path = f"{path}/{child_key}"
                child_paths.append(f"/{child_path}") # type: ignore
                walk(child_node, child_path) # type: ignore

        if child_paths:
            flat_node["childs"] = child_paths

        result[full_path] = flat_node

    for key, node in dialogs.items():
        walk(node, key)

    return result


def prev_path(path: str) -> str:
    parts = path.strip('/').split('/')

    if len(parts) <= 1:
        return '/'

    return '/' + '/'.join(parts[:-1])


def include_nodes(obj: dict[str, Any], DEBUG: bool) -> dict[str, Any]:
    if DEBUG:
        return obj
    return {}