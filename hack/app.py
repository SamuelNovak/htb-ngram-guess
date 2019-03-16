import json
from flask import Flask, jsonify, request

from . import game

app = Flask(__name__)

@app.route('/samo-htb/event')
def event():
    print(request.get_json())
    ncco = [{
            "action": "talk",
            "text": game.challenge_wording(game.create_challenge()),
            "voiceName": "Amy",
            "bargeIn": False
        }]
    return jsonify(ncco)

@app.route("/samo-htb/answer")
def answer_call():
    ncco = [
        {
            "action": "connect",
            "from": "NEXMO_NUMBER",
            "endpoint": [{
                "type": 'mobile',
                "number": "__"
            }]
        }, {
            "action": "talk",
            "text": "Welcome to the N gram guesser game. The point of the game is to guess which word combination was the most common is a specified year. Enjoy!",
            "voiceName": "Amy",
            "bargeIn": False
        }, {
            "action": "talk",
            "text": "Press 1, to start the game, followed by the hash key.",
            "voiceName": "Amy",
            "bargeIn": True
        }, {
            "action": "input",
            "submitOnHash": True,
            "timeOut": 10
        }
    ]
    return jsonify(ncco)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)