#!/bin/bash
# HeartGuard AI — Launch Flask Backend API
# Run from the HeartDisease project directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv/bin"

echo "HeartGuard AI — Flask API Server"
echo "================================="

# Retrain model if artifacts are missing
if [ ! -f "$SCRIPT_DIR/heart_disease_model.pkl" ] || [ ! -f "$SCRIPT_DIR/model_metadata.json" ]; then
    echo "[INFO] Model artifacts not found. Running train_model.py first..."
    "$VENV/python3" "$SCRIPT_DIR/train_model.py"
fi

echo "[INFO] Starting Flask API on http://localhost:5050"
"$VENV/python3" "$SCRIPT_DIR/server.py"
