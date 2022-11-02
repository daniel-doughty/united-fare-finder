#!/bin/sh
python3 -m venv venv
source "./venv/bin/activate"
pip install -r requirements.txt
python3 -u united-fare-finder.py > output.txt
deactivate
