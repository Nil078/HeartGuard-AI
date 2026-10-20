"""Deterministic clinical risk factor and lifestyle recommendation rules.

Pure rule engine: functions evaluate submitted clinical values deterministically
without calling ML models. All thresholds are defined in one place for auditable review.
"""

from __future__ import annotations

from typing import Any, Callable

# ── 1. Clinical Risk Factor Rules ─────────────────────────────────────────────
# Each rule maps a lambda(form_data) -> bool to a human-readable label.
# Thresholds follow standard ACC/AHA and clinical screening guidelines.
RISK_FACTOR_RULES: list[dict[str, Any]] = [
    {
        "id": "bp_elevated",
        "condition": lambda d: float(d.get("trestbps", 0)) >= 140,
        "label": "Elevated resting blood pressure (>= 140 mm Hg)",
    },
    {
        "id": "chol_high",
        "condition": lambda d: float(d.get("chol", 0)) >= 240,
        "label": "High serum cholesterol level (>= 240 mg/dl)",
    },
    {
        "id": "fbs_high",
        "condition": lambda d: int(d.get("fbs", 0)) == 1,
        "label": "Fasting blood sugar above normal range (> 120 mg/dl)",
    },
    {
        "id": "exang_present",
        "condition": lambda d: int(d.get("exang", 0)) == 1,
        "label": "Exercise-induced angina present",
    },
    {
        "id": "thalach_low",
        "condition": lambda d: float(d.get("thalach", 200)) < (220 - float(d.get("age", 50))) * 0.70,
        "label": "Reduced maximum heart rate during exercise for age (< 70% age-predicted max)",
    },
    {
        "id": "oldpeak_high",
        "condition": lambda d: float(d.get("oldpeak", 0)) >= 2.0,
        "label": "Significant exercise ST depression (Oldpeak >= 2.0 mm)",
    },
    {
        "id": "ca_present",
        "condition": lambda d: int(d.get("ca", 0)) >= 1,
        "label": "Major vessel involvement detected on fluoroscopy (ca >= 1)",
    },
    {
        "id": "thal_defect",
        "condition": lambda d: int(d.get("thal", 2)) in (1, 3),
        "label": "Perfusion defect indicated on Thalassemia test (Fixed or Reversible defect)",
    },
]

# ── 2. Lifestyle & Dietary Suggestions ─────────────────────────────────────────
# Each rule provides a {title, reason} pair referencing the specific submitted values.
LIFESTYLE_RULES: list[dict[str, Any]] = [
    {
        "condition": lambda d: float(d.get("chol", 0)) >= 240,
        "title": "Prefer soluble-fiber-rich foods (oats, pulses, legumes, apples, berries)",
        "reason": "Your recorded serum cholesterol is elevated ({chol} mg/dl; target is typically < 200 mg/dl).",
    },
    {
        "condition": lambda d: float(d.get("chol", 0)) >= 240,
        "title": "Limit saturated and industrial trans fats",
        "reason": "Reduces LDL cholesterol accumulation and vascular strain.",
    },
    {
        "condition": lambda d: float(d.get("trestbps", 0)) >= 140,
        "title": "Adopt a low-sodium diet (DASH pattern) and reduce added salt",
        "reason": "Your resting blood pressure is elevated ({trestbps} mm Hg; normal resting target is < 120 mm Hg).",
    },
    {
        "condition": lambda d: float(d.get("trestbps", 0)) >= 140,
        "title": "Increase dietary potassium from natural sources (bananas, spinach, beans)",
        "reason": "Supports healthy vascular tone when blood pressure is elevated.",
    },
    {
        "condition": lambda d: int(d.get("fbs", 0)) == 1,
        "title": "Limit added sugars, sweetened beverages, and refined carbohydrates",
        "reason": "Your fasting blood sugar indicator is flagged above the 120 mg/dl reference threshold.",
    },
    {
        "condition": lambda d: int(d.get("fbs", 0)) == 1,
        "title": "Prioritize complex carbohydrates with low glycemic index",
        "reason": "Assists in stabilizing post-meal glycemic response and insulin sensitivity.",
    },
    {
        "condition": lambda d: int(d.get("exang", 0)) == 1 or float(d.get("oldpeak", 0)) >= 2.0,
        "title": "Discuss a physician-guided exercise and activity plan",
        "reason": "Exercise-related chest pain or significant ST depression was reported during exertion.",
    },
    {
        "condition": lambda d: True,  # Baseline routine check
        "title": "Schedule routine blood pressure and lipid profile checks",
        "reason": "Recommended periodic cardiovascular monitoring regardless of current values.",
    },
    {
        "condition": lambda d: True,  # Baseline sleep & stress
        "title": "Prioritize 7-8 hours of quality sleep and stress-reduction routines",
        "reason": "Consistent restorative sleep directly benefits autonomic and cardiovascular regulation.",
    },
]


def evaluate_risk_factors(form_data: dict[str, Any]) -> list[str]:
    """Evaluate submitted form data against clinical risk rules.
    
    Returns a list of human-readable factor descriptions. Empty list if none triggered.
    """
    flagged: list[str] = []
    for rule in RISK_FACTOR_RULES:
        try:
            if rule["condition"](form_data):
                flagged.append(rule["label"])
        except Exception:
            continue
    return flagged


def evaluate_lifestyle_suggestions(form_data: dict[str, Any]) -> list[dict[str, str]]:
    """Evaluate submitted form data against lifestyle and dietary rules.
    
    Returns a list of dicts with 'title' and dynamically formatted 'reason'.
    """
    suggestions: list[dict[str, str]] = []
    for rule in LIFESTYLE_RULES:
        try:
            if rule["condition"](form_data):
                reason_template = rule["reason"]
                reason_formatted = reason_template.format(
                    chol=form_data.get("chol", "N/A"),
                    trestbps=form_data.get("trestbps", "N/A"),
                    age=form_data.get("age", "N/A"),
                    thalach=form_data.get("thalach", "N/A"),
                )
                suggestions.append({
                    "title": rule["title"],
                    "reason": reason_formatted,
                })
        except Exception:
            continue
    return suggestions
