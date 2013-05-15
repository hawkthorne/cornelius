import flask
import os
from raven import Client

app = flask.Flask(__name__)
client = Client(os.environ.get('SENTRY_DSN', ''))


@app.route("/errors", methods=["POST"])
def errors():
    payload = flask.request.json

    if payload is None or not isinstance(payload, dict):
        return flask.jsonify(message="Could not decode JSON object"), 400

    if 'message' not in payload:
        return flask.jsonify(message="Key 'message' is required in JSON payload"), 400

    message = payload['message']
    tags = payload.get('tags', {})

    request_id = client.captureMessage(message, tags=tags)
    return flask.jsonify(success=True, request_id=request_id), 201


if __name__ == "__main__":
    app.run(debug=True)
