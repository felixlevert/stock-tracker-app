#!/bin/sh
export FLASK_APP=./src/__init__.py
python -m flask run -h 0.0.0.0 -p 5001