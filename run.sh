#!/bin/bash
# run.sh - sets up and runs the whole project with one command.
# Usage:  bash run.sh

echo "Setting up virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
pytest -v

echo "Starting the app..."
streamlit run app.py
