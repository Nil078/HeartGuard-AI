"""Input validation for the Prediction page."""

from __future__ import annotations

from typing import Any

NUMERIC_RULES = {
    "age": {"min": 1, "max": 120, "label": "Age", "integer": True, "unit": "years"},
    "trestbps": {
        "min": 60,
        "max": 260,
        "label": "Resting blood pressure",
        "integer": True,
        "unit": "mm Hg",
    },
    "chol": {
        "min": 80,
        "max": 700,
        "label": "Cholesterol",
        "integer": True,
        "unit": "mg/dl",
    },
    "thalach": {
        "min": 50,
        "max": 250,
        "label": "Maximum heart rate",
        "integer": True,
        "unit": "bpm",
    },
    "oldpeak": {
        "min": 0.0,
        "max": 10.0,
        "label": "Oldpeak (ST depression)",
        "integer": False,
        "unit": "",
    },
    "ca": {
        "min": 0,
        "max": 3,
        "label": "Number of major vessels",
        "integer": True,
        "unit": "",
    },
}

CATEGORICAL_RULES = {
    "sex": {"allowed": [0, 1], "label": "Sex"},
    "cp": {"allowed": [0, 1, 2, 3], "label": "Chest pain type"},
    "fbs": {"allowed": [0, 1], "label": "Fasting blood sugar"},
    "restecg": {"allowed": [0, 1, 2], "label": "Resting ECG"},
    "exang": {"allowed": [0, 1], "label": "Exercise-induced angina"},
    "slope": {"allowed": [0, 1, 2], "label": "Slope of peak exercise ST segment"},
    "thal": {"allowed": [1, 2, 3], "label": "Thalassemia"},
}

FIELD_RULES = {**NUMERIC_RULES, **CATEGORICAL_RULES}


def validate_inputs(form_data: dict[str, Any]) -> list[str]:
    """Return human-readable error messages. Empty list means the form is valid."""
    errors: list[str] = []
    
    # Check numeric fields
    for field, rule in NUMERIC_RULES.items():
        if field not in form_data or form_data[field] is None:
            errors.append(f"{rule['label']} is required.")
            continue
        value = form_data[field]
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            errors.append(f"{rule['label']} must be a number.")
            continue
        if rule["integer"] and abs(numeric - round(numeric)) > 1e-9:
            errors.append(f"{rule['label']} must be a whole number.")
            continue
        if numeric < rule["min"] or numeric > rule["max"]:
            unit = f" {rule['unit']}" if rule["unit"] else ""
            errors.append(
                f"{rule['label']} must be between {rule['min']} and {rule['max']}{unit}."
            )

    # Check categorical fields
    for field, rule in CATEGORICAL_RULES.items():
        if field not in form_data or form_data[field] is None:
            errors.append(f"{rule['label']} selection is required.")
            continue
        value = form_data[field]
        if value not in rule["allowed"]:
            errors.append(f"Invalid selection for {rule['label']}.")

    return errors

