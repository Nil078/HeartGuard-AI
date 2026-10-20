"""Preprocessing helpers shared by training and the Streamlit UI.

Numeric vs categorical columns are listed explicitly (several categoricals are
stored as integers). Encodings used by the Prediction form live here so the
UI and training pipeline never drift apart.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "heart_disease.csv"

NUMERIC_FEATURES: list[str] = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak",
    "ca",
]
CATEGORICAL_FEATURES: list[str] = [
    "sex",
    "cp",
    "fbs",
    "restecg",
    "exang",
    "slope",
    "thal",
]
FEATURE_COLUMNS: list[str] = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]
TARGET_COLUMN = "target"

# Human-readable labels → values present in data/heart_disease.csv (Kaggle
# recoding of the UCI Cleveland set). This is the single source of truth.
FEATURE_ENCODINGS: dict[str, dict[str, int]] = {
    "sex": {"Female": 0, "Male": 1},
    "cp": {
        "Typical Angina": 0,
        "Atypical Angina": 1,
        "Non-anginal Pain": 2,
        "Asymptomatic": 3,
    },
    "fbs": {"No": 0, "Yes": 1},
    "restecg": {
        "Normal": 0,
        "ST-T Wave Abnormality": 1,
        "Left Ventricular Hypertrophy": 2,
    },
    "exang": {"No": 0, "Yes": 1},
    "slope": {"Upsloping": 0, "Flat": 1, "Downsloping": 2},
    "thal": {
        "Normal": 2,
        "Fixed Defect": 1,
        "Reversible Defect": 3,
    },
}

# Display labels for analysis charts (encoded integer → label).
CATEGORY_DISPLAY: dict[str, dict[int, str]] = {
    key: {code: label for label, code in mapping.items()}
    for key, mapping in FEATURE_ENCODINGS.items()
}
CATEGORY_DISPLAY["thal"][0] = "Unknown / missing"


def load_raw_dataset(path: Path | None = None) -> pd.DataFrame:
    csv_path = path or DATA_PATH
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {csv_path}. Place heart_disease.csv in data/."
        )
    return pd.read_csv(csv_path, encoding="utf-8-sig")


def dataset_diagnostics(df: pd.DataFrame) -> dict[str, Any]:
    """Collect (do not print) dataset diagnostics used by train_model.py."""
    invalid: dict[str, Any] = {}
    if "ca" in df.columns:
        bad_ca = df.loc[~df["ca"].between(0, 3), "ca"]
        if len(bad_ca):
            invalid["ca_out_of_range"] = {
                "count": int(len(bad_ca)),
                "values": sorted(bad_ca.dropna().unique().tolist()),
            }
    if "thal" in df.columns:
        # In this CSV, 0 is not a valid clinical code (1/2/3 after recoding).
        bad_thal = df.loc[~df["thal"].isin([1, 2, 3]), "thal"]
        if len(bad_thal):
            invalid["thal_unknown"] = {
                "count": int(len(bad_thal)),
                "values": sorted(bad_thal.dropna().unique().tolist()),
            }
    non_numeric = []
    for col in FEATURE_COLUMNS + [TARGET_COLUMN]:
        if col not in df.columns:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            non_numeric.append(col)
    if non_numeric:
        invalid["non_numeric_columns"] = non_numeric

    target_counts = (
        df[TARGET_COLUMN].value_counts(dropna=False).sort_index().to_dict()
        if TARGET_COLUMN in df.columns
        else {}
    )
    return {
        "shape": list(df.shape),
        "columns": df.columns.tolist(),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "missing": {c: int(v) for c, v in df.isna().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "class_distribution_raw": {str(k): int(v) for k, v in target_counts.items()},
        "invalid_values": invalid,
        "head": df.head(5).to_dict(orient="records"),
    }


def binarize_target(y: pd.Series) -> tuple[pd.Series, dict[str, Any]]:
    """Map multi-class Cleveland target to binary: 0 vs any value > 0."""
    before = y.value_counts(dropna=False).sort_index().to_dict()
    unique = pd.Series(y.dropna().unique())
    if unique.nunique() > 2 or (unique.min() == 0 and unique.max() > 1):
        y_bin = (y.astype(float) > 0).astype(int)
        note = "Mapped target: 0 → No Heart Disease, any value > 0 → 1 (Heart Disease)."
    else:
        y_bin = y.astype(int)
        note = "Target already binary (0 / 1); no remapping applied."
    after = y_bin.value_counts(dropna=False).sort_index().to_dict()
    return y_bin, {
        "note": note,
        "before": {str(k): int(v) for k, v in before.items()},
        "after": {str(k): int(v) for k, v in after.items()},
    }


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Apply only the cleaning steps this file actually needs. Returns notes."""
    notes: list[str] = []
    cleaned = df.copy()
    cleaned.columns = [str(c).replace("\ufeff", "").strip() for c in cleaned.columns]

    n_dup = int(cleaned.duplicated().sum())
    if n_dup:
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)
        notes.append(f"Dropped {n_dup} duplicate row(s).")
    else:
        notes.append("No duplicate rows found; none dropped.")

    if cleaned.isna().sum().sum() == 0:
        notes.append("No missing values in the raw file.")
    else:
        notes.append(
            "Missing values present; numeric columns will be median-imputed and "
            "categorical columns mode-imputed inside the training pipeline "
            "(fit on X_train only)."
        )

    if "ca" in cleaned.columns:
        n_bad_ca = int((~cleaned["ca"].between(0, 3)).sum())
        if n_bad_ca:
            cleaned.loc[~cleaned["ca"].between(0, 3), "ca"] = pd.NA
            notes.append(
                f"Set {n_bad_ca} out-of-range ca value(s) (outside 0–3) to missing "
                "for median imputation inside the pipeline."
            )
        else:
            notes.append("All ca values were already in 0–3.")

    if "thal" in cleaned.columns:
        n_bad_thal = int((~cleaned["thal"].isin([1, 2, 3])).sum())
        if n_bad_thal:
            cleaned.loc[~cleaned["thal"].isin([1, 2, 3]), "thal"] = pd.NA
            notes.append(
                f"Set {n_bad_thal} unknown thal value(s) (not in {{1, 2, 3}}) to missing "
                "for most-frequent imputation inside the pipeline."
            )
        else:
            notes.append("All thal values were already in {1, 2, 3}.")

    if TARGET_COLUMN in cleaned.columns and "oldpeak" in cleaned.columns:
        # Clinical alignment: In Kaggle's Cleveland recoding, 0 was disease and 1 was healthy.
        # Align to standard clinical diagnostic definition: 1 = Heart Disease Detected, 0 = No Heart Disease.
        try:
            if float(cleaned["oldpeak"].corr(cleaned[TARGET_COLUMN])) < 0:
                cleaned[TARGET_COLUMN] = (cleaned[TARGET_COLUMN].astype(int) == 0).astype(int)
                notes.append(
                    "Aligned target labels to clinical convention: 1 = Heart Disease Detected, 0 = No Heart Disease."
                )
        except Exception:
            pass

    return cleaned, notes


def split_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y


def _one_hot_encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:  # scikit-learn < 1.2
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_preprocessor(scale_numeric: bool) -> ColumnTransformer:
    """ColumnTransformer: impute + optional scale for numeric; OHE for categorical."""
    numeric_steps: list[tuple[str, Any]] = [
        ("imputer", SimpleImputer(strategy="median")),
    ]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))
    numeric_pipe = Pipeline(numeric_steps)
    categorical_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", _one_hot_encoder()),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, NUMERIC_FEATURES),
            ("cat", categorical_pipe, CATEGORICAL_FEATURES),
        ]
    )


def form_data_to_dataframe(form_data: dict[str, Any]) -> pd.DataFrame:
    """Build a single-row DataFrame in training column order from UI values."""
    row = {col: form_data[col] for col in FEATURE_COLUMNS}
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)
