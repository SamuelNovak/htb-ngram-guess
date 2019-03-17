import nexmo
import json
from flask import Flask, jsonify, request

from . import game, db

with open("ngram_guesser/config.json") as f:
    config = json.loads(f.read())

app = Flask(__name__)
dbcon = db.connect(config)

# players = {"NUMBER": ["CHALLENGE=None", "POINTS=0"]}
players = {}
# calls = {"CON_UUID": "NUMBER"}
calls = {}

@app.route('/api/event', methods=["GET", "POST"])
def event():
    if request.is_json:
        req = request.get_json()
    elif request.method == "GET":
        req = request.args.to_dict()
    else:
        req = request.form.to_dict()
    print(req)
    con_uuid = req["conversation_uuid"]

    if "dtmf" in req:
        player = calls[con_uuid]
        if not player in players:
            players[player] = db.load_player(dbcon, player)

        if players[player][0] == None: # new challenge
            challenge = game.create_challenge()
            players[player][0] = challenge
            ncco = [{
                    "action": "talk",
                    "text": game.challenge_wording(challenge),
                    "voiceName": "Amy",
                    "bargeIn": False
                }, {
                    "action": "input",
                    "submitOnHash": True,
                    "timeOut": 10
                }]
        else:
            challenge = players[player][0]
            choice = int(req["dtmf"])
            if 0 <= choice < 4:
                answer = challenge["guesses"][choice]
                points, message = game.evaluate_challenge(challenge, answer)
                players[player][1] += points
                players[player][0] = None
                db.save_player(dbcon, player, players[player][1])
                ncco = [{
                        "action": "talk",
                        "text": message + "You now have a total of {} points.".format(players[player][1]),
                        "voiceName": "Amy",
                        "bargeIn": False
                    }, {
                        "action": "talk",
                        "text": "Press 1, followed by the hash key, to continue the game.",
                        "voiceName": "Amy",
                        "bargeIn": True
                    }, {
                        "action": "input",
                        "submitOnHash": True,
                        "timeOut": 10
                    }]
            else:
                ncco = [{
                        "action": "talk",
                        "text": "You pressed the invalid or no key. Try again.",
                        "voiceName": "Amy",
                        "bargeIn": False
                    }, {
                        "action": "talk",
                        "text": game.challenge_wording(challenge),
                        "voiceName": "Amy",
                        "bargeIn": False
                    }, {
                        "action": "input",
                        "submitOnHash": True,
                        "timeOut": 10
                    }]
        return jsonify(ncco)
    else: # TODO: Handle call end, so I can get rid of the con_uid in the dict
        return jsonify([])

@app.route("/api/answer", methods=["GET", "POST"])
def answer_call():
    if request.is_json:
        req = request.get_json()
    elif request.method == "GET":
        req = request.args.to_dict()
    else:
        req = request.form.to_dict()
    con_uuid = req["conversation_uuid"]
    caller = req["from"]
    calls[con_uuid] = caller

    ncco = [
        {
            "action": "talk",
            "text": "Welcome to the bigram guesser game. The point of the game is to guess which word combination was the most common is a specified year. Enjoy!",
            "voiceName": "Amy",
            "bargeIn": False
        }, {
            "action": "talk",
            "text": "Press 1, followed by the hash key, to start the game.",
            "voiceName": "Amy",
            "bargeIn": True
        }, {
            "action": "input",
            "submitOnHash": True,
            "timeOut": 10
        }
    ]
    return jsonify(ncco)

@app.route('/api/sms', methods=['GET', 'POST'])
def inbound_sms():
    if request.is_json:
        req = request.get_json()
    elif request.method == "GET":
        req = request.args.to_dict()
    else:
        req = request.form.to_dict()

    return ('', 204)

@app.route("/api/makecall", methods=["POST"])
def makecall():
    if request.is_json:
        req = request.get_json()
    else:
        req = request.form.to_dict()
    try:
        to_number = req["to"]
    except:
        return "Invalid query."

    client = nexmo.Client(application_id=config["appid"], private_key="ngram_guesser/private.key")
    try:
        response = client.create_call({
            'to': [{'type': 'mobile', 'number': to_number}],
            'from': {'type': 'mobile', 'number': config["number"]},
            'answer_url': ['http://35.230.134.67/api/answer'],
            'answer_method': "POST",
            "event_url": ["http://35.230.134.67/api/event"],
            "event_method": "POST"
            })
        return str(response)
    except:
        return "Error!"


@app.route("/")
def index():
    lb = db.load_leaderboard(dbcon)
    table = "".join(["<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(i + 1, ("*" * (len(lb[i]) - 4)) + lb[i][0][-4:], str(lb[i][1])) for i in range(len(lb))])
    with open("ngram_guesser/template.html", "r") as f:
        return f.read().replace("{placeholder}", table)

def close():
    dbcon.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
    close()