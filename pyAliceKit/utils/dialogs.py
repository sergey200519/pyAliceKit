from typing import Any, Callable, Optional, TypeVar, cast


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

def flatten_dialogs(
    node: DialogNode,
    path: str = "",
    result: Optional[dict[str, DialogNode]] = None
) -> dict[str, DialogNode]:
    if result is None:
        result = {}

    result[path] = node

    childs: dict[str, DialogNode] = node.get("childs", {})
    for key, child in childs.items():
        new_path = f"{path}/{key}" if path else key
        flatten_dialogs(child, new_path, result)

    return result