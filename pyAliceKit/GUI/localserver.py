# pyAliceKit/GUI/localserver.py

import http.server
import importlib
import json
import socketserver
import os
import traceback
from pathlib import Path
from types import ModuleType
from typing import Any

from pyAliceKit.GUI.utils.html import get_html_template
from pyAliceKit.GUI.views.get.settings import get_all_settings

PORT = 8081

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, settings: ModuleType, **kwargs: Any) -> None:
        self.settings = settings
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(get_html_template("index.html", Path(__file__)).encode('utf-8'))

        elif self.path.endswith(".html"):
            html_file = self.path.lstrip("/")
            try:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(get_html_template(html_file, Path(__file__)).encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, f"{html_file} not found")

        elif self.path == "/api/settings/get_all":
            try:
                importlib.reload(self.settings)
                data: dict[Any, Any] = get_all_settings(self.settings)
                json_bytes: str = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(json_bytes)))
                self.end_headers()
                self.wfile.write(json_bytes)

            except Exception as e:
                traceback.print_exc()
                error_message = {"error": str(e)}
                error_bytes = json.dumps(error_message, ensure_ascii=False).encode("utf-8")

                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(error_bytes)))
                self.end_headers()
                self.wfile.write(error_bytes)

        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/settings/change_simple":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode("utf-8"))

                key = data.get("key")
                value = data.get("value")

                if not hasattr(self.settings, key):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": f"Ключ '{key}' не найден в settings"}).encode("utf-8"))
                    return

                current_value = getattr(self.settings, key)
                new_value = self._cast_value(value, type(current_value))
                setattr(self.settings, key, new_value)

                print(f"KEY: {key} | RAW VALUE: {value} | CASTED VALUE: {new_value}")
                print("SETTINGS_PATH:", Path(self.settings.__file__).resolve())

                self._update_settings_file(key, new_value)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "key": key,
                    "value": new_value
                }, ensure_ascii=False).encode("utf-8"))

            except Exception as e:
                traceback.print_exc()
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def _cast_value(self, value: Any, expected_type: type) -> Any:
        try:
            if expected_type == bool:
                if isinstance(value, str):
                    return value.lower() == "true"
                return bool(value)
            elif expected_type == int:
                return int(value)
            elif expected_type == float:
                return float(value)
            elif expected_type in (list, dict) and isinstance(value, str):
                return json.loads(value)
            return expected_type(value)
        except Exception:
            return value

    def _update_settings_file(self, key: str, value: Any):
        """Обновляет значение переменной в settings.py, зная путь из модуля"""
        file_path = Path(self.settings.__file__).resolve()

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        updated = False
        for line in lines:
            if line.strip().startswith(f"{key} ="):
                python_value = self._python_repr(value)
                new_lines.append(f"{key} = {python_value}\n")
                updated = True
            else:
                new_lines.append(line)

        if updated:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

    def _python_repr(self, value: Any) -> str:
        """Преобразует Python-объект в валидную строку для settings.py"""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return "True" if value else "False"
        else:
            return json.dumps(value, ensure_ascii=False)


def run(settings: ModuleType):
    static_dir = Path(__file__).parent / "static"
    os.chdir(static_dir)

    def handler_with_settings(*args: Any, **kwargs: Any) -> RequestHandler:
        return RequestHandler(*args, settings=settings, **kwargs)

    with socketserver.TCPServer(("", PORT), handler_with_settings) as httpd:
        print(f"🚀 Local server running at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    # run()
    pass
