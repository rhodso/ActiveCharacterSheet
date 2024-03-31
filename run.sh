#!/bin/bash

echo "Detecting if Python is installed..."
python_version=$(python --version 2>&1)

if [[ -z $python_version ]]; then
    echo "Python is not installed."
    echo "Please install Python and try again."
    exit 1
fi

python_major=$(echo $python_version | awk -F. '{print $2}')

if [[ $python_major -lt 3 ]]; then
    echo "Python version is less than 3.7."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

if [[ $python_major -lt 3 ]]; then
    echo "Python version is less than 3.11."
    echo "Please note that Python 3.11 or higher is recommended for this project."
fi

echo "Python is installed. Version: $python_version"
echo "Detecting if virtual environment is activated..."

if [[ ! -f ".venv/pyvenv.cfg" ]]; then
    echo "Creating virtual environment in .venv directory."
    python -m venv .venv
fi

if [[ -z $VIRTUAL_ENV ]]; then
    echo "Virtual environment is not activated."
    echo "Activating virtual environment in .venv directory."
    source .venv/bin/activate
else
    echo "Virtual environment is already activated."
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running main.py with additional arguments: $@"
python MainUI.py "$@"
