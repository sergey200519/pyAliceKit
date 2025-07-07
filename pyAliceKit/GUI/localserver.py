# pyAliceKit/GUI/localserver.py

import http.server
import importlib
import json
import socketserver
import os
from pathlib import Path
from types import ModuleType
from typing import Any

from pyAliceKit.GUI.utils.html import get_html_template
from pyAliceKit.GUI.views.get.settings import get_all_settings

SETTINGS_PATH = Path(__file__).parent.parent / "settings.py"
PORT = 8080

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
            # Удаляем ведущий слеш и загружаем HTML-файл из templates
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
                error_message = {"error": str(e)}
                error_bytes = json.dumps(error_message, ensure_ascii=False).encode("utf-8")

                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(error_bytes)))
                self.end_headers()
                self.wfile.write(error_bytes)
        else:
            # Обработка других запросов, например, статических файлов
            super().do_GET()

    def do_POST(self):
        pass


def run(settings: ModuleType):
    static_dir = Path(__file__).parent / "static"
    os.chdir(static_dir)

    # Обёртка, которая передаёт settings в RequestHandler
    def handler_with_settings(*args: Any, **kwargs: Any) -> RequestHandler:
        return RequestHandler(*args, settings=settings, **kwargs)

    with socketserver.TCPServer(("", PORT), handler_with_settings) as httpd:
        print(f"🚀 Local server running at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    # run()
    pass
