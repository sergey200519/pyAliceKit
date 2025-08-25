# #!/usr/bin/env python3
# import argparse
# import subprocess
# from flask import Flask
# from pyAliceKit.GUI.localserver import run
# from testing import settings
# from pyAliceKit.py_alice.py_alice import PyAlice

# def runserver():
#     from flask import request, jsonify

#     app = Flask(__name__)
#     pyAlice = PyAlice(settings) # type: ignore

#     @app.route("/", methods=["GET", "POST"])
#     def alice_handler(): # type: ignore
#         if not request.is_json:
#             return jsonify({"error": "Expected application/json"})
#         response = pyAlice.get_response_for_alice(type="dict")
#         return jsonify(response)

#     app.run(port=5000)

# def map_nodes():
#     pass

# def run_dev_ui():
#     # Например, запуск локального UI на FastAPI, Flask или с помощью subprocess на npm run dev
#     subprocess.run(["python", "-m", "http.server", "8000"], cwd="dev_ui")  # Пример
#     # или, если это FastAPI:
#     # subprocess.run(["uvicorn", "dev_ui.app:app", "--reload"])

# # def run_server():
# #     HOST = "localhost"
# #     PORT = 8080
# #     with http.server.HTTPServer((HOST, PORT), AliceRequestHandler) as httpd:
# #         print(f"Сервер запущен на http://{HOST}:{PORT}")
# #         httpd.serve_forever()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="CLI for managing AliceKit skill project.")
#     parser.add_argument("command", choices=["start", "map_nodes", "dev_ui"])

#     args = parser.parse_args()

#     if args.command == "start":
#         runserver()
#     elif args.command == "map_nodes":
#         map_nodes()
#     elif args.command == "dev_ui":
#         run(settings)








#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import time
import signal
from pathlib import Path
from pyAliceKit.GUI.localserver import run
from testing import settings
from pyAliceKit.py_alice.py_alice import PyAlice


def runserver():
    from flask import Flask, request, jsonify

    app = Flask(__name__)
    pyAlice = PyAlice(settings)  # type: ignore

    @app.route("/", methods=["GET", "POST"])
    def alice_handler():  # type: ignore
        if not request.is_json:
            return jsonify({"error": "Expected application/json"})
        response = pyAlice.get_response_for_alice(type="dict")
        return jsonify(response)

    app.run(port=5000)


def map_nodes():
    print("🔧 Генерация карты диалога...")
    # TODO: реализовать


def terminate_process_gracefully(process: subprocess.Popen, timeout=5):
    """Попытка аккуратно завершить процесс."""
    if process.poll() is not None:
        return  # Уже завершён

    try:
        process.send_signal(signal.SIGINT)
        process.wait(timeout=timeout)
        return
    except subprocess.TimeoutExpired:
        pass

    try:
        process.terminate()  # SIGTERM
        process.wait(timeout=timeout)
        return
    except subprocess.TimeoutExpired:
        pass

    # Если процесс всё ещё жив, убиваем принудительно
    process.kill()
    process.wait()


def run_dev_ui():
    from pathlib import Path

    def get_all_py_files(root: Path):
        return [f for f in root.rglob("*.py") if 'venv' not in str(f) and '__pycache__' not in str(f)]

    def get_mtimes(files):
        return {str(f): f.stat().st_mtime for f in files}

    while True:
        files = get_all_py_files(Path("pyAliceKit")) + get_all_py_files(Path("testing"))
        mtimes = get_mtimes(files)

        try:
            process = subprocess.Popen([
                sys.executable,
                "-c",
                (
                    "from pyAliceKit.GUI.localserver import run; "
                    "from testing import settings; "
                    "run(settings)"
                )
            ])
            print("🚀 dev_ui сервер запущен...")

        except OSError as e:
            print(f"❌ Ошибка запуска сервера: {e}")
            time.sleep(1)
            continue

        try:
            while True:
                time.sleep(1)
                new_files = get_all_py_files(Path("pyAliceKit")) + get_all_py_files(Path("testing"))
                new_mtimes = get_mtimes(new_files)

                if any(mtimes.get(str(f), 0) != new_mtimes.get(str(f), 0) for f in new_mtimes):
                    print("🔄 Изменение файлов обнаружено, перезапуск...")
                    terminate_process_gracefully(process)
                    # Небольшая задержка перед повторным запуском, чтобы порт освободился
                    time.sleep(1)
                    break

                mtimes = new_mtimes

        except KeyboardInterrupt:
            print("🛑 Остановка разработки")
            terminate_process_gracefully(process)
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for managing AliceKit skill project.")
    parser.add_argument("command", choices=["start", "map_nodes", "dev_ui"])

    args = parser.parse_args()

    if args.command == "start":
        runserver()
    elif args.command == "map_nodes":
        map_nodes()
    elif args.command == "dev_ui":
        run_dev_ui()
