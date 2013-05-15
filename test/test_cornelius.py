import json
import cornelius
from nose.tools import assert_equals


client = cornelius.app.test_client()

def test_no_json():
    resp = client.post("/errors")
    assert_equals(400, resp.status_code)


def test_json_non_object():
    resp = client.post("/errors", headers={"Content-Type": "application/json"},
                       data=json.dumps([]))
    assert_equals(400, resp.status_code)


def test_json_missing_message():
    resp = client.post("/errors", data=json.dumps({}),
                       content_type='application/json')
    assert_equals(400, resp.status_code)

def test_json_message():
    resp = client.post("/errors", data=json.dumps({'message': 'foo'}),
                       content_type='application/json')
    assert_equals(201, resp.status_code)
    assert_equals(None, json.loads(resp.data)['request_id'])
