#!/usr/bin/env bash
# run.sh - Launcher for Coaching Center Student Result Management System on macOS / Linux

set -e

# Change directory to project root
cd "$(dirname "$0")"

# Activate virtual environment if present
if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
fi

# Run with python3 or fallback to python
if command -v python3 >/dev/null 2>&1; then
    exec python3 main.py "$@"
elif command -v python >/dev/null 2>&1; then
    exec python main.py "$@"
else
    echo "[ERROR] Python 3 is required but could not be found on PATH." >&2
    exit 1
fi
