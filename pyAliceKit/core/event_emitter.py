from typing import Any, Callable, Self


class EventEmitter:
    def __init__(self: Self) -> None:
        self.__listeners: dict[str, list[Callable[..., Any]]] = {}

    def on(self: Self, event_name: str, handler: Callable[..., Any]) -> None:
        self.__listeners.setdefault(event_name, []).append(handler)

    def emit(self: Self, event_name: str, event: dict[str, Any], *args: Any, **kwargs: Any) -> None:
        for handler in self.__listeners.get(event_name, []):
            handler(event, *args, **kwargs)  # type: ignore



event_emitter = EventEmitter()

def on_event(event_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        event_emitter.on(event_name, func)
        return func
    return decorator