import base64
import os
import json
import logging

import requests
import flask
import raven
from raven.contrib.flask import Sentry

app = flask.Flask(__name__)
app.config['SENTRY_DSN'] = os.environ.get('SENTRY_DSN', '')
client = raven.Client(os.environ.get('LOVE_DSN', ''))
sentry = Sentry(app)


def track(event, properties):
    if not event:
        return

    token = os.environ.get('MIXPANEL_TOKEN', None)

    if token is None:
        return

    logging.error(flask.request.headers.get('X-Forwarded-For'))
    
    if 'X-Forwarded-For' in flask.request.headers:
        ips = flask.request.headers['X-Forwarded-For'].split(",")
        properties['ip'] = ips[0]

    params = {
        'event': event,
        'properties': properties,
    }

    data = base64.b64encode(json.dumps(params))
    url = "http://api.mixpanel.com/track/?data=" + data

    return requests.get(url)



@app.route("/metrics", methods=["POST"])
def metrics():
    payload = flask.request.json

    if payload is None or not isinstance(payload, dict):
        return flask.jsonify(message="Could not decode JSON object"), 400

    if 'metrics' not in payload:
        return flask.jsonify(message="Key 'metrics' is required in JSON payload"), 400

    for metric in payload['metrics']:
        track(metric.get('event'), metric.get('properties', {}))

    return flask.jsonify(success=True), 201


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
