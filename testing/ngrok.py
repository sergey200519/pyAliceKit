from flask import Flask, request, jsonify
from pyAliceKit.py_alice.py_alice import PyAlice
from testing import settings

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def alice_handler(): # type: ignore
    print(request)
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type. Expected application/json."}), 415
    

    event = request.get_json()
    pyAlice = PyAlice(params_alice=event, settings=settings) # type: ignore
    
    # Предположим, что текст генерируется методом pyAlice.get_response_text() или аналогичным
    # text = "TEEST"  # Здесь должен быть ваш текст ответа, полученный из pyAlice

    # response = { # type: ignore
    #     "version": event.get("version"),
    #     "session": event.get("session"),
    #     "response": {
    #         "text": text,
    #         "end_session": False
    #     },
    #     "session_state": {
    #         "trainnnnnnn": "test",
    #         "nummmmm": 1234567890
    #     }
    # }
    response = pyAlice.get_response_for_alice(type="dict")
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)
