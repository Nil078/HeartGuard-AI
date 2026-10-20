"""Heart Disease Detection ML Backend Server.

Provides REST API endpoints for cardiovascular risk prediction, real model metadata,
exploratory dataset statistics, and downloadable clinical PDF reports.
Serves the modern HeartGuard AI web application frontend.
"""

from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd

from utils.preprocessing import (
    CATEGORY_DISPLAY,
    DATA_PATH,
    FEATURE_COLUMNS,
    FEATURE_ENCODINGS,
    form_data_to_dataframe,
    load_raw_dataset,
)
from utils.report_generator import generate_patient_pdf
from utils.risk_rules import evaluate_lifestyle_suggestions, evaluate_risk_factors
from utils.validation import validate_inputs

PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_ROOT / "public" if (PROJECT_ROOT / "public").exists() else PROJECT_ROOT / "static"


def _resolve_asset_path(filename: str) -> Path:
    candidates = [
        PROJECT_ROOT / filename,
        Path.cwd() / filename,
        Path(__file__).resolve().parent / filename,
        Path(__file__).resolve().parent.parent / filename,
        Path("/var/task") / filename,
        Path("/var/task/HeartDisease") / filename,
    ]
    for c in candidates:
        if c.exists():
            return c
    return PROJECT_ROOT / filename


MODEL_PATH = _resolve_asset_path("heart_disease_model.pkl")
METADATA_PATH = _resolve_asset_path("model_metadata.json")

app = Flask(__name__, static_folder=str(STATIC_DIR))
CORS(app)

# ── Load Model & Metadata at Startup ──────────────────────────────────────────
model = None
metadata = None
dataset_stats = None


def init_app():
    global model, metadata, dataset_stats

    # Load trained model pipeline
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        print(f"Loaded ML model: {type(model)}")
    else:
        print("Warning: heart_disease_model.pkl not found!")

    # Load model metadata
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        print(f"Loaded metadata. Best engine: {metadata.get('best_model_name')}")
    else:
        print("Warning: model_metadata.json not found!")

    # Pre-calculate dataset summary statistics
    try:
        df = load_raw_dataset()
        dataset_stats = compute_dataset_stats(df)
        print(f"Computed dataset statistics for {len(df)} patient records.")
    except Exception as exc:
        print(f"Error computing dataset statistics: {exc}")


def compute_dataset_stats(df: pd.DataFrame) -> dict[str, Any]:
    """Compute aggregate distributions from the Cleveland dataset for EDA visuals."""
    # Target distribution
    target_counts = df["target"].value_counts().to_dict()
    # Sex distribution
    sex_counts = df["sex"].value_counts().to_dict()
    # Chest pain type distribution
    cp_counts = df["cp"].value_counts().to_dict()

    # Numerical metrics grouped by target
    grouped = df.groupby("target")
    means_by_target = grouped[["age", "trestbps", "chol", "thalach", "oldpeak"]].mean().to_dict()

    # Age buckets
    age_bins = [0, 40, 50, 60, 70, 100]
    age_labels = ["<40", "40-49", "50-59", "60-69", "70+"]
    df["age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=False)
    age_dist = df.groupby(["age_group", "target"], observed=False).size().unstack(fill_value=0).to_dict()

    return {
        "total_records": len(df),
        "target_distribution": {
            "no_disease": int(target_counts.get(0, 0)),
            "disease_detected": int(target_counts.get(1, 0)),
        },
        "sex_distribution": {
            "female": int(sex_counts.get(0, 0)),
            "male": int(sex_counts.get(1, 0)),
        },
        "chest_pain_distribution": {
            "typical_angina": int(cp_counts.get(0, 0)),
            "atypical_angina": int(cp_counts.get(1, 0)),
            "non_anginal": int(cp_counts.get(2, 0)),
            "asymptomatic": int(cp_counts.get(3, 0)),
        },
        "means_by_target": {
            k: {int(t): round(float(v), 2) for t, v in vals.items()}
            for k, vals in means_by_target.items()
        },
        "age_distribution": {
            label: {
                "no_disease": int(age_dist.get(0, {}).get(label, 0)),
                "disease_detected": int(age_dist.get(1, {}).get(label, 0)),
            }
            for label in age_labels
        },
    }


# ── Static Web App Routes ─────────────────────────────────────────────────────

@app.route("/")
def serve_index():
    return send_from_directory(str(STATIC_DIR), "index.html")


@app.route("/<path:path>")
def serve_static(path: str):
    # Reject API subpaths falling through
    if path.startswith("api/"):
        return jsonify({"error": f"API endpoint not found: /{path}"}), 404

    file_path = STATIC_DIR / path
    if file_path.exists() and file_path.is_file():
        return send_from_directory(str(STATIC_DIR), path)

    # Return 404 for missing assets (CSS, JS, images) so browser doesn't get index.html
    if any(path.endswith(ext) for ext in [".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".json", ".woff", ".woff2", ".ttf"]):
        return f"Asset not found: {path}", 404

    # Single-page navigation fallback
    return send_from_directory(str(STATIC_DIR), "index.html")


# ── API Endpoints (Dual /api/* and /* routes to handle Vercel rewrites) ────────

@app.route("/api", methods=["GET"])
@app.route("/api/", methods=["GET"])
@app.route("/api/index", methods=["GET", "POST", "OPTIONS"])
@app.route("/api/index.py", methods=["GET", "POST", "OPTIONS"])
def vercel_entrypoint_fallback():
    if request.args.get("debug"):
        return jsonify({
            "path": request.path,
            "headers": dict(request.headers),
            "environ_keys": [k for k in request.environ.keys() if "HTTP" in k or "URI" in k or "PATH" in k]
        })

    # Header sources for original URI before rewrite
    raw = (
        request.headers.get("X-Forwarded-Uri", "")
        or request.headers.get("X-Original-Url", "")
        or request.environ.get("REQUEST_URI", "")
        or request.args.get("__route", "")
    )

    if request.method == "POST":
        if "report" in raw:
            return download_report()
        return predict()

    if "metadata" in raw:
        return get_metadata()
    if "dataset" in raw:
        return get_dataset_stats()

    return health()


@app.route("/api/health", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "best_model_name": metadata.get("best_model_name") if metadata else None,
        "trained_at": metadata.get("trained_at") if metadata else None,
        "features": FEATURE_COLUMNS,
    })


@app.route("/api/debug-env", methods=["GET"])
def debug_env():
    env_vars = {
        k: str(v)
        for k, v in request.environ.items()
        if isinstance(v, (str, int, float, bool)) and "SECRET" not in k and "KEY" not in k
    }
    return jsonify({
        "path": request.path,
        "environ_path_info": request.environ.get("PATH_INFO"),
        "environ_query_string": request.environ.get("QUERY_STRING"),
        "headers": dict(request.headers),
        "env_vars": env_vars,
    })


@app.route("/api/metadata", methods=["GET"])
@app.route("/metadata", methods=["GET"])
def get_metadata():
    if metadata is None:
        return jsonify({"error": "Model metadata not loaded"}), 500
    return jsonify(metadata)


@app.route("/api/dataset", methods=["GET"])
@app.route("/dataset", methods=["GET"])
@app.route("/api/dataset/stats", methods=["GET"])
@app.route("/dataset/stats", methods=["GET"])
def get_dataset_stats():
    if dataset_stats is None:
        return jsonify({"error": "Dataset statistics not available"}), 500
    return jsonify(dataset_stats)


@app.route("/api/predict", methods=["POST"])
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Machine learning model is not available"}), 503

    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request: JSON body required"}), 400

    # Ensure correct data types according to Cleveland feature specifications
    try:
        parsed_data = {
            "age": int(data.get("age", 0)),
            "sex": int(data.get("sex", 0)),
            "cp": int(data.get("cp", 0)),
            "trestbps": int(data.get("trestbps", 0)),
            "chol": int(data.get("chol", 0)),
            "fbs": int(data.get("fbs", 0)),
            "restecg": int(data.get("restecg", 0)),
            "thalach": int(data.get("thalach", 0)),
            "exang": int(data.get("exang", 0)),
            "oldpeak": float(data.get("oldpeak", 0.0)),
            "slope": int(data.get("slope", 0)),
            "ca": int(data.get("ca", 0)),
            "thal": int(data.get("thal", 2)),
        }
    except (ValueError, TypeError) as exc:
        return jsonify({"error": f"Invalid field format: {exc}"}), 400

    # Validate against ACC/AHA and dataset range rules
    validation_errors = validate_inputs(parsed_data)
    if validation_errors:
        return jsonify({"error": "Validation failed", "validation_errors": validation_errors}), 422

    try:
        # Convert to 1-row DataFrame matching trained Pipeline schema
        X = form_data_to_dataframe(parsed_data)

        # Execute real inference through scikit-learn Pipeline
        pred = int(model.predict(X)[0])
        proba = model.predict_proba(X)[0]
        classes = list(model.classes_)
        proba_map = {int(c): float(p) for c, p in zip(classes, proba)}
        p0 = float(proba_map.get(0, 0.0))
        p1 = float(proba_map.get(1, 0.0))

        # Evaluate deterministic clinical risk rules & lifestyle recommendations
        risk_factors = evaluate_risk_factors(parsed_data)
        lifestyle_suggestions = evaluate_lifestyle_suggestions(parsed_data)

        best_model_name = metadata.get("best_model_name", "Logistic Regression") if metadata else "Logistic Regression"

        return jsonify({
            "predicted_class": pred,
            "prediction_label": "Heart Disease Detected" if pred == 1 else "No Heart Disease Detected",
            "is_high_risk": pred == 1,
            "probability_no_disease": round(p0, 4),
            "probability_heart_disease": round(p1, 4),
            "risk_score_percent": round(p1 * 100.0, 1),
            "model_name": best_model_name,
            "risk_factors": risk_factors,
            "lifestyle_suggestions": lifestyle_suggestions,
            "patient_values": parsed_data,
            "disclaimer": (
                "For educational purposes only. This system is a student machine-learning project "
                "and does not constitute clinical medical diagnosis. Consult a licensed healthcare provider."
            ),
        })
    except Exception as exc:
        return jsonify({"error": f"Inference execution failed: {str(exc)}"}), 500


@app.route("/api/report", methods=["POST"])
@app.route("/report", methods=["POST"])
def download_report():
    if model is None or metadata is None:
        return jsonify({"error": "Model or metadata not ready"}), 503

    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request: JSON body required"}), 400

    try:
        parsed_data = {
            "age": int(data.get("age", 0)),
            "sex": int(data.get("sex", 0)),
            "cp": int(data.get("cp", 0)),
            "trestbps": int(data.get("trestbps", 0)),
            "chol": int(data.get("chol", 0)),
            "fbs": int(data.get("fbs", 0)),
            "restecg": int(data.get("restecg", 0)),
            "thalach": int(data.get("thalach", 0)),
            "exang": int(data.get("exang", 0)),
            "oldpeak": float(data.get("oldpeak", 0.0)),
            "slope": int(data.get("slope", 0)),
            "ca": int(data.get("ca", 0)),
            "thal": int(data.get("thal", 2)),
        }
    except (ValueError, TypeError) as exc:
        return jsonify({"error": f"Invalid field format: {exc}"}), 400

    # Run inference to get ground-truth prediction
    X = form_data_to_dataframe(parsed_data)
    pred = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0]
    classes = list(model.classes_)
    proba_map = {int(c): float(p) for c, p in zip(classes, proba)}
    p0 = float(proba_map.get(0, 0.0))
    p1 = float(proba_map.get(1, 0.0))

    risk_factors = evaluate_risk_factors(parsed_data)
    lifestyle_suggestions = evaluate_lifestyle_suggestions(parsed_data)

    best_model_name = metadata.get("best_model_name", "Logistic Regression")
    trained_at = metadata.get("trained_at", "")

    pdf_bytes = generate_patient_pdf(
        form_data=parsed_data,
        predicted_class=pred,
        proba_0=p0,
        proba_1=p1,
        model_name=best_model_name,
        trained_at=trained_at,
        risk_factors=risk_factors,
        lifestyle_suggestions=lifestyle_suggestions,
    )

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="HeartGuard_Patient_Assessment_Report.pdf",
    )


@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith("/api"):
        return jsonify({"error": f"API endpoint not found: {request.path}"}), 404
    file_path = STATIC_DIR / "index.html"
    if file_path.exists():
        return send_from_directory(str(STATIC_DIR), "index.html")
    return "Not Found", 404


@app.errorhandler(405)
def handle_405(e):
    if request.path.startswith("/api"):
        return jsonify({"error": f"Method {request.method} not allowed on {request.path}"}), 405
    return "Method Not Allowed", 405


@app.errorhandler(500)
def handle_500(e):
    if request.path.startswith("/api"):
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
    return "Internal Server Error", 500


# Initialize model and metadata before serving
init_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    print(f"Starting Heart Disease Detection Server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
