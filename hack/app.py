import json
from flask import Flask, jsonify, request

from . import game

app = Flask(__name__)

# players = {"NUMBER": ("CHALLENGE=None", "POINTS=0")}
players = {}
# calls = {"CON_UUID": "NUMBER"}
calls = {}

@app.route('/samo-htb/event', methods=["GET", "POST"])
def event():
    if request.is_json:
        req = request.get_json()
    else:
        req = {k:v for (k,v) in request.iteritems()}
    print(req)
    con_uuid = req["conversation_uuid"]
    status = req["status"]

    if status == "input":
        player = calls[con_uuid]
        if not player in players:
            players[player] = (None, 0)

        if players[player][0] == None: # new challenge
            players[player][0] = game.create_challenge()
            ncco = [{
                    "action": "talk",
                    "text": game.challenge_wording(game.create_challenge()),
                    "voiceName": "Amy",
                    "bargeIn": False
                }, {
                    "action": "input",
                    "submitOnHash": True,
                    "timeOut": 10
                }]
        else:
            challenge = players[player][0]
            answer = challenge["guesses"][req.dtmf]
            points, message = game.evaluate_challenge(challenge, answer)
            players[player][1] += points
            players[player][0] = None
            ncco = [{
                    "action": "talk",
                    "text": message + "You now have a total of {} points.".format(players[player][1]),
                    "voiceName": "Amy",
                    "bargeIn": False
                }, {
                    "action": "talk",
                    "text": "Press 1, to continue the game, followed by the hash key.",
                    "voiceName": "Amy",
                    "bargeIn": True
                }, {
                    "action": "input",
                    "submitOnHash": True,
                    "timeOut": 10
                }]

        return jsonify(ncco)
    else:
        return jsonify([])

@app.route("/samo-htb/answer", methods=["GET", "POST"])
def answer_call():
    if request.is_json:
        req = request.get_json()
    else:
        req = {k:v for (k,v) in request.iteritems()}
    con_uuid = req["conversation_uuid"]
    caller = req["from"]
    calls[con_uuid] = caller

    ncco = [
        {
        #     "action": "connect",
        #     "from": "NEXMO_NUMBER",
        #     "endpoint": [{
        #         "type": 'mobile',
        #         "number": "__"
        #     }]
        # }, {
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