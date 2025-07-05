import http.server
import json
from pyAliceKit.py_alice.py_alice import PyAlice

HOST = "localhost"
PORT = 8080

# Создаём объект PyAlice
# pyAlice = PyAlice(settings={})  # Передай настройки, если нужно

class AliceRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
            pyAlice.load_request(data)
            response = pyAlice.get_response_for_alice(type="dict")
            response_bytes = json.dumps(response, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
        except Exception as e:
            error_response = {"error": str(e)}
            self.send_response(500)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode("utf-8"))

    def do_GET(self):
        # Простая HTML-форма для ручного ввода JSON
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")

        self.end_headers()
        html = f"""
        <html>
        <body>
            <h1>pyAliceKit Debugger</h1>
            <form method="POST" action="/" enctype="application/json" onsubmit="submitForm(event)">
                <textarea id="json" rows="20" cols="80">{{}}</textarea><br>
                <button type="submit">Отправить</button>
            </form>
            <pre id="response"></pre>
            <script>
            async function submitForm(e) {{
                e.preventDefault();
                const text = document.getElementById("json").value;
                const res = await fetch("/", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json"
                    }},
                    body: text
                }});
                const data = await res.text();
                document.getElementById("response").textContent = data;
            }}
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

def run_server():
    with http.server.HTTPServer((HOST, PORT), AliceRequestHandler) as httpd:
        print(f"Сервер запущен на http://{HOST}:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
