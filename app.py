import flask

app = flask.Flask(__name__)

@app.route("/")
def index():
    return "Hello World!", 201

app.run()