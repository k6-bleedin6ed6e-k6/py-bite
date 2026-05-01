#!/usr/bin/env bash
set -e

# Try common venv names
for VENV_DIR in ".venv" "venv"; do
    if [ -d "$VENV_DIR/bin" ]; then
        source "$VENV_DIR/bin/activate"
        break
    elif [ -d "$VENV_DIR/Scripts" ]; then
        source "$VENV_DIR/Scripts/activate"
        break
    fi
done

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment not found. Run: bash install.sh"
    exit 1
fi

python run.py
