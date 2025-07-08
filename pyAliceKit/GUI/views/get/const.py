from __future__ import annotations
import json
import importlib
from typing import TYPE_CHECKING, Optional

from typing import Any
from urllib.parse import urlparse, parse_qs

import inspect
import traceback

if TYPE_CHECKING:
    from pyAliceKit.GUI.localserver import RequestHandler


def safe_json(obj: dict[Any, Any] | list[Any] | tuple[Any, ...] | str | int | float | bool | None) -> dict[Any, Any] | list[Any] | tuple[Any, ...] | str | int | float | bool | None:
    if isinstance(obj, dict):
        return {k: safe_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [safe_json(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(safe_json(item) for item in obj)
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif inspect.isfunction(obj) or inspect.ismethod(obj):
        try:
            source = inspect.getsource(obj)
            return source
        except Exception:
            return f"<function {obj.__name__}>"
    else:
        try:
            json.dumps(obj)
            return obj
        except TypeError:
            return f"<unsupported: {type(obj).__name__}>"

def get_const(http: RequestHandler) -> Optional[dict[Any, Any]]:
    try:
        importlib.reload(http.settings)

        query = urlparse(http.path).query
        params = parse_qs(query)
        key = params.get("key", [None])[0]

        
        if key:
            if hasattr(http.settings, key):
                raw_value = getattr(http.settings, key)
                response: dict[Any, Any] = {key: safe_json(raw_value)}
            else:
                http.send_response(404)
                http.send_header("Content-Type", "application/json; charset=utf-8")
                http.end_headers()
                http.wfile.write(json.dumps({"error": f"Ключ '{key}' не найден в settings"}).encode("utf-8"))
                return
        else:
            # Если параметр key не передан — вернуть все безопасные константы
            response = {
                k: safe_json(v)
                for k, v in http.settings.__dict__.items()
                if not k.startswith("__") and not callable(v)
            }

        json_bytes = json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8")

        http.send_response(200)
        http.send_header("Content-Type", "application/json; charset=utf-8")
        http.send_header("Content-Length", str(len(json_bytes)))
        http.end_headers()
        http.wfile.write(json_bytes)

    except Exception as e:
        traceback.print_exc()
        error_message = {"error": str(e)}
        error_bytes = json.dumps(error_message, ensure_ascii=False).encode("utf-8")

        http.send_response(500)
        http.send_header("Content-Type", "application/json; charset=utf-8")
        http.send_header("Content-Length", str(len(error_bytes)))
        http.end_headers()
        http.wfile.write(error_bytes)
