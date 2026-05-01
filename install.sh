#!/usr/bin/env bash
set -e

PROJECT_NAME="python-tutor"
PYTHON_CMD=""
VENV_DIR="venv"

echo "========================================"
echo "  Python Tutor - Installer"
echo "========================================"

# Detect uv (preferred)
if command -v uv &> /dev/null; then
    USE_UV=1
    echo "Detected uv — using uv for fast setup."
else
    USE_UV=0
fi

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

PY_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Detected Python $PY_VERSION at $(which $PYTHON_CMD)"

# Check minimum version
MIN_VERSION="3.8"
if [ "$(printf '%s\n' "$MIN_VERSION" "$PY_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo "Error: Python $MIN_VERSION or higher is required. Found $PY_VERSION."
    exit 1
fi

# Move into project directory if running from repo root
if [ -d "$PROJECT_NAME" ]; then
    cd "$PROJECT_NAME"
fi

if [ "$USE_UV" -eq 1 ]; then
    VENV_DIR=".venv"
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment with uv..."
        uv venv
    fi
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    echo "Installing dependencies with uv..."
    uv pip install -r requirements.txt
else
    # Create virtual environment
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
    fi

    # Activate virtual environment
    echo "Activating virtual environment..."
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    elif [ -f "$VENV_DIR/Scripts/activate" ]; then
        source "$VENV_DIR/Scripts/activate"
    else
        echo "Error: Could not activate virtual environment."
        exit 1
    fi

    # Upgrade pip
    echo "Upgrading pip..."
    pip install --quiet --upgrade pip

    # Install dependencies
    echo "Installing dependencies from requirements.txt..."
    pip install --quiet -r requirements.txt
fi

# Create data directory and progress file if missing
mkdir -p data
if [ ! -f "data/progress.json" ]; then
    echo '{}' > data/progress.json
fi

echo ""
echo "========================================"
echo "  Installation complete!"
echo "========================================"
echo ""
echo "To start the app:"
echo "  bash run.sh"
echo ""
echo "Or manually:"
echo "  source $VENV_DIR/bin/activate && python run.py"
echo ""
echo "Then open http://localhost:5000 in your browser."
