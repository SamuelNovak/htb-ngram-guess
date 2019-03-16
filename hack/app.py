from flask import Flask
app = Flask(__name__)

@app.route('/api/event')
def event():
    return 'Hello, World!'

@app.route("/api/")
