.PHONY: test install serve

install: venv
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -r test/requirements.txt

test: venv
	venv/bin/nosetests test

venv:
	virtualenv venv

serve:
	venv/bin/python cornelius.py
