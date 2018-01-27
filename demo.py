import flask
from jsonapi import JsonApi, JsonObj

app = flask.Flask(__name__)


class Api(JsonApi):
    pass


@app.route('/')
def main():
    return api(request.json())

if __name__ == '__main__':
    app.run(debug=True)
