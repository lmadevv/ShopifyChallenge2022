#!/bin/bash
source venv/Scripts/activate
export FLASK_APP=application.py
export FLASK_ENV=development
flask run
