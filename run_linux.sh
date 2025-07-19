#!/bin/bash
VENV_DIR="venv"

function cleanup {
    deactivate
    exit 1
}

trap cleanup INT

if [ ! -d "$VENV_DIR" ]; then
    echo "No virtual environment found. Creating..."
    python3 -m venv "$VENV_DIR"
    
    source "$VENV_DIR/bin/activate"
    
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    else
        echo "File requirements.txt not found. No dependency installed."
    fi

    echo "Environment Installed, running..."
else
    echo "Environment already installed, running..."
    source "$VENV_DIR/bin/activate"
fi

python init.py
deactivate
