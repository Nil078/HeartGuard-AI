"""Offline training script for HeartGuard AI.

Loads data/heart_disease.csv, logs diagnostics, cleans, splits (once), tunes
candidate models with CV on the training fold only, evaluates on the held-out
test set, and writes heart_disease_model.pkl + model_metadata.json.

This script is the only place that calls .fit(). The Streamlit app never retrains.
"""

from __future__ import annotations

import json
import traceback
import warnings
from datetime import datetime, timezone

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from utils.model_utils import (
    METADATA_PATH,
    MODEL_PATH,
    evaluate_model,
    extract_feature_importance,
    json_safe,
    select_best_model,
)
from utils.preprocessing import (
    CATEGORICAL_FEATURES,
    DATA_PATH,
    FEATURE_COLUMNS,
    NUMERIC_FEATURES,
    binarize_target,
    build_preprocessor,
    clean_dataset,
    dataset_diagnostics,
    load_raw_dataset,
    split_xy,
)

warnings.filterwarnings("ignore", category=UserWarning)

CV = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
TEST_SIZE = 0.20
RANDOM_STATE = 42

# Tree-based models skip StandardScaler; linear/distance models use it.
MODEL_SPECS: list[dict] = [
    {
        "name": "Logistic Regression",
        "scale": True,
        "estimator": LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
        "param_grid": {"model__C": [0.1, 1.0, 10.0]},
    },
    {
        "name": "Decision Tree",
        "scale": False,
        "estimator": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "param_grid": {
            "model__max_depth": [3, 5, 7, None],
            "model__min_samples_split": [2, 5, 10],
        },
    },
    {
        "name": "Random Forest",
        "scale": False,
        "estimator": RandomForestClassifier(random_state=RANDOM_STATE),
        "param_grid": {
            "model__n_estimators": [50, 100],
            "model__max_depth": [3, 5, 7],
            "model__min_samples_split": [2, 5],
        },
    },
    {
        "name": "Gradient Boosting",
        "scale": False,
        "estimator": GradientBoostingClassifier(random_state=RANDOM_STATE),
        "param_grid": {
            "model__n_estimators": [50, 100],
            "model__learning_rate": [0.05, 0.1],
            "model__max_depth": [2, 3],
        },
    },
    {
        "name": "Support Vector Machine",
        "scale": True,
        "estimator": SVC(kernel="rbf", probability=True, random_state=RANDOM_STATE),
        "param_grid": {"model__C": [0.1, 1.0, 10.0], "model__gamma": ["scale"]},
    },
    {
        "name": "K-Nearest Neighbors",
        "scale": True,
        "estimator": KNeighborsClassifier(),
        "param_grid": {
            "model__n_neighbors": [3, 5, 7, 9],
            "model__weights": ["uniform", "distance"],
        },
    },
]


def _try_xgboost() -> dict | None:
    try:
        from xgboost import XGBClassifier
    except Exception as exc:  # noqa: BLE001 — skip cleanly if missing
        print(f"\n[XGBoost] Skipping: could not import xgboost ({exc}).")
        return None
    return {
        "name": "XGBoost",
        "scale": False,
        "estimator": XGBClassifier(
            random_state=RANDOM_STATE,
            eval_metric="logloss",
            n_jobs=1,
        ),
        "param_grid": {
            "model__n_estimators": [50, 100],
            "model__max_depth": [3, 5],
            "model__learning_rate": [0.05, 0.1],
        },
    }


def print_diagnostics(raw: pd.DataFrame, diag: dict) -> None:
    print("=" * 72)
    print("DATASET DIAGNOSTICS")
    print("=" * 72)
    print(f"Path: {DATA_PATH}")
    print(f"Shape: {diag['shape']}")
    print("\nFirst 5 rows:")
    print(raw.head(5).to_string(index=False))
    print("\nColumn names and dtypes:")
    for col, dtype in diag["dtypes"].items():
        print(f"  {col:12s} {dtype}")
    print("\nMissing-value counts:")
    for col, n in diag["missing"].items():
        print(f"  {col:12s} {n}")
    print(f"\nDuplicate row count: {diag['duplicate_rows']}")
    print(f"Class distribution of target (raw): {diag['class_distribution_raw']}")
    print(f"Invalid / out-of-range values: {diag['invalid_values'] or 'none detected'}")
    print("=" * 72)


def train_one(spec: dict, X_train, y_train, X_test, y_test) -> tuple[Pipeline, dict]:
    pipe = Pipeline(
        [
            ("preprocessor", build_preprocessor(scale_numeric=spec["scale"])),
            ("model", spec["estimator"]),
        ]
    )
    search = GridSearchCV(
        pipe,
        spec["param_grid"],
        cv=CV,
        scoring="roc_auc",
        n_jobs=1,
        refit=True,
    )
    search.fit(X_train, y_train)
    best_pipe: Pipeline = search.best_estimator_
    metrics = evaluate_model(best_pipe, X_test, y_test)
    metrics["best_params"] = json_safe(search.best_params_)
    metrics["cv_best_roc_auc"] = float(search.best_score_)
    importance = extract_feature_importance(best_pipe)
    if importance is None:
        metrics["feature_importance"] = None
        metrics["feature_importance_note"] = (
            f"{spec['name']} does not expose feature_importances_ or coef_; skipped."
        )
        print(f"  Feature importance: skipped ({metrics['feature_importance_note']})")
    else:
        metrics["feature_importance"] = importance
    print(
        f"  Test  acc={metrics['accuracy']:.4f}  prec={metrics['precision']:.4f}  "
        f"rec={metrics['recall']:.4f}  f1={metrics['f1']:.4f}  "
        f"roc-auc={metrics['roc_auc']:.4f}  cv-auc={metrics['cv_best_roc_auc']:.4f}"
    )
    print(f"  Best params: {search.best_params_}")
    return best_pipe, metrics


def main() -> None:
    print("\nHeartGuard AI — training run\n")
    raw = load_raw_dataset()
    diag = dataset_diagnostics(raw)
    print_diagnostics(raw, diag)

    cleaned, clean_notes = clean_dataset(raw)
    X, y_raw = split_xy(cleaned)
    y, target_info = binarize_target(y_raw)
    print("\nTARGET BINARIZATION")
    print(f"  {target_info['note']}")
    print(f"  Before: {target_info['before']}")
    print(f"  After:  {target_info['after']}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(
        f"\nSplit: test_size={TEST_SIZE}, random_state={RANDOM_STATE}, stratify=y"
        f"\n  X_train={X_train.shape}  X_test={X_test.shape}"
        f"\n  y_train class counts: {y_train.value_counts().sort_index().to_dict()}"
        f"\n  y_test  class counts: {y_test.value_counts().sort_index().to_dict()}"
    )
    print(
        "\nPreprocessing is inside each Pipeline. Scalers/encoders are fit on "
        "X_train only via GridSearchCV (StratifiedKFold within the training fold)."
    )

    specs = list(MODEL_SPECS)
    xgb_spec = _try_xgboost()
    xgb_omission = None
    if xgb_spec is not None:
        specs.append(xgb_spec)
    else:
        xgb_omission = "XGBoost omitted because the package was not importable."

    pipelines: dict[str, Pipeline] = {}
    comparison: dict[str, dict] = {}
    print("\nTRAINING / TUNING (GridSearchCV, scoring=roc_auc)\n")
    for spec in specs:
        print(f"- {spec['name']} (scale_numeric={spec['scale']})")
        try:
            pipe, metrics = train_one(spec, X_train, y_train, X_test, y_test)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAILED: {exc}")
            traceback.print_exc()
            continue
        pipelines[spec["name"]] = pipe
        comparison[spec["name"]] = metrics

    if not comparison:
        raise RuntimeError("No models trained successfully.")

    best_name, rationale = select_best_model(comparison)
    best_pipeline = pipelines[best_name]
    print("\nCOMPARISON (test set)")
    print(f"{'Model':<24} {'Acc':>8} {'Prec':>8} {'Rec':>8} {'F1':>8} {'AUC':>8}")
    for name, m in comparison.items():
        mark = " *" if name == best_name else ""
        print(
            f"{name:<24} {m['accuracy']:8.4f} {m['precision']:8.4f} "
            f"{m['recall']:8.4f} {m['f1']:8.4f} {m['roc_auc']:8.4f}{mark}"
        )
    print(f"\nSelection rationale:\n  {rationale}")

    preprocessing_notes = " ".join(clean_notes + [target_info["note"]])
    print("\nPREPROCESSING REPORT")
    for note in clean_notes:
        print(f"  - {note}")
    print(f"  - {target_info['note']}")
    if xgb_omission:
        print(f"  - {xgb_omission}")

    class_dist = y.value_counts().sort_index().to_dict()
    best_importance = comparison[best_name].get("feature_importance")

    metadata = {
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "best_model_name": best_name,
        "selection_rationale": rationale,
        "feature_names": FEATURE_COLUMNS,
        "categorical_features": CATEGORICAL_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "preprocessing_notes": preprocessing_notes,
        "preprocessing_report": clean_notes + [target_info["note"]],
        "dataset_shape": list(cleaned.shape),
        "dataset_shape_raw": diag["shape"],
        "class_distribution": {str(k): int(v) for k, v in class_dist.items()},
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "model_comparison": json_safe(comparison),
        "feature_importance": json_safe(best_importance),
        "xgboost_omission": xgb_omission,
        "diagnostics": {
            "missing": diag["missing"],
            "duplicate_rows": diag["duplicate_rows"],
            "invalid_values": diag["invalid_values"],
            "target_binarization": target_info,
        },
        "limitations": [
            "Dataset size may be limited.",
            "Results may not generalize to all populations.",
            "This is a screening/educational tool, not a diagnostic system.",
        ],
    }

    joblib.dump(best_pipeline, MODEL_PATH)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(json_safe(metadata), f, indent=2)

    print(f"\nSaved {MODEL_PATH.name}")
    print(f"Saved {METADATA_PATH.name}")
    print("Done.\n")


if __name__ == "__main__":
    main()
