# pyAliceKit/GUI/localserver.py

import http.server
import json
import socketserver
import os
import traceback
from pathlib import Path
from types import ModuleType
from typing import Any

from pyAliceKit.GUI.utils.html import get_html_template
from pyAliceKit.GUI.views.get.get_dialog_nodes import get_dialog_nodes
from pyAliceKit.GUI.views.get.settings import get_all_settings
from pyAliceKit.GUI.views.post.settings_change_simple import post_settings_change_simple

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
                data: dict[Any, Any] = get_all_settings(self.settings)
                json_bytes: str = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8") # type: ignore

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(json_bytes)))
                self.end_headers()
                self.wfile.write(json_bytes) # type: ignore

            except Exception as e:
                traceback.print_exc()
                error_message = {"error": str(e)}
                error_bytes = json.dumps(error_message, ensure_ascii=False).encode("utf-8")

                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(error_bytes)))
                self.end_headers()
                self.wfile.write(error_bytes)
        elif self.path == "/api/settings/get_dialog_nodes":
            get_dialog_nodes(self)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/settings/change_simple":
            post_settings_change_simple(self)


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
