#!/bin/bash
# HeartGuard AI — Launch Streamlit Dashboard
# Run from the HeartDisease project directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv/bin"

echo "HeartGuard AI — Streamlit Dashboard"
echo "====================================="

# Retrain model if artifacts are missing
if [ ! -f "$SCRIPT_DIR/heart_disease_model.pkl" ] || [ ! -f "$SCRIPT_DIR/model_metadata.json" ]; then
    echo "[INFO] Model artifacts not found. Running train_model.py first..."
    "$VENV/python3" "$SCRIPT_DIR/train_model.py"
fi

echo "[INFO] Starting Streamlit on http://localhost:8501"
"$VENV/streamlit" run "$SCRIPT_DIR/app.py" --server.port 8501
