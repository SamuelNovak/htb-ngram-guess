import json
from flask import Flask, jsonify, 


app = Flask(__name__)

@app.route('/samo-htb/event')
def event():
    print(request.get_json())
    return 'Hello, World!'

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
        }
    ]
    return jsonify(ncco)

if __name__ == '__main__':
    app.run(port=80)