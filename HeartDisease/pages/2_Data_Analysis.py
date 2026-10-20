"""Data Analysis Page — Data Insights & Exploratory Clinical Analytics.

Matches Stitch Screen: "Data Insights & Analytics" (ID: 0e572ef52e6a4f1c8d834005d4e816da)
"""

from __future__ import annotations

import streamlit as st

from utils.preprocessing import FEATURE_COLUMNS, TARGET_COLUMN
from utils.styling import (
    disclaimer_card,
    load_css,
    render_nav_bar,
    render_sidebar,
    section_title,
    topbar,
)
from utils.visualization import (
    chart_by_target,
    chart_class_balance,
    chart_correlation,
    chart_feature_importance,
    chart_histogram,
    load_cleaned_dataset,
    load_metadata_cached,
)

st.set_page_config(
    page_title="Data Insights & Analytics | HeartGuard AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
metadata = load_metadata_cached()
render_sidebar("Data Analysis")
topbar("Data Insights & Analytics", metadata)
render_nav_bar("Data Analysis")
disclaimer_card("eda")

# ── Load Dataset ──────────────────────────────────────────────────────────────
try:
    df, notes = load_cleaned_dataset()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.stop()

# Cleaning notes expander
with st.expander("Dataset Diagnostics & Preprocessing Documentation", expanded=False):
    for note in notes:
        st.write(f"- {note}")
    if metadata and metadata.get("preprocessing_notes"):
        st.caption(metadata["preprocessing_notes"])

# ── Target Class Balance & Overview ───────────────────────────────────────────
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
section_title("🎯 Outcome Distribution (Target Class Balance)")
st.plotly_chart(chart_class_balance(df), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Feature Distributions Grid ────────────────────────────────────────────────
section_title("📊 Biometric Distributions (Cleveland Cohort)")
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_histogram(df, "age", "Patient Age Distribution", "Age in Years"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_histogram(df, "trestbps", "Resting Blood Pressure Distribution", "mm Hg"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_histogram(df, "chol", "Serum Cholesterol Distribution", "mg/dl"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_histogram(df, "thalach", "Max Heart Rate Achieved Distribution", "bpm"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Target-Stratified Analysis & Interactive Biomarker Explorer ───────────────
section_title("🔬 Comparative Biomarkers vs Cardiovascular Outcome")

st.markdown('<div class="glass-panel" style="margin-bottom: 1rem;">', unsafe_allow_html=True)
st.markdown("<div style='font-size:0.92rem; font-weight:700; color:#ff4455; margin-bottom:8px;'>Interactive Clinical Feature Explorer (All 13 Biometric Variables)</div>", unsafe_allow_html=True)

exp_col1, exp_col2 = st.columns([2, 1])
with exp_col1:
    selected_feature = st.selectbox(
        "Select Clinical Biometric Attribute to Analyze:",
        options=FEATURE_COLUMNS,
        format_func=lambda col: {
            "age": "Age (years)",
            "sex": "Sex (0=Female, 1=Male)",
            "cp": "Chest Pain Type (0-3)",
            "trestbps": "Resting Blood Pressure (mm Hg)",
            "chol": "Serum Cholesterol (mg/dl)",
            "fbs": "Fasting Blood Sugar > 120 (0=No, 1=Yes)",
            "restecg": "Resting ECG Results (0-2)",
            "thalach": "Max Heart Rate Achieved (bpm)",
            "exang": "Exercise-Induced Angina (0=No, 1=Yes)",
            "oldpeak": "ST Depression 'Oldpeak' (mm)",
            "slope": "Slope of Peak Exercise ST Segment (0-2)",
            "ca": "Major Fluoroscopy Vessels (0-3)",
            "thal": "Thalassemia Scan (1=Normal, 2=Fixed, 3=Reversible)",
        }.get(col, col),
        index=0,
    )
with exp_col2:
    plot_kind = st.selectbox("Visualization Type:", ["box", "hist"], format_func=lambda x: "Box / Whisker Plot" if x == "box" else "Distribution Histogram")

st.plotly_chart(
    chart_by_target(
        df,
        selected_feature,
        f"{selected_feature.upper()} Stratification vs Cardiovascular Diagnosis",
        kind=plot_kind,
    ),
    use_container_width=True,
)
st.markdown('</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_by_target(df, "sex", "Diagnosis Distribution by Biological Sex", kind="hist"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_by_target(df, "cp", "Diagnosis Distribution by Chest Pain Category", kind="hist"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Feature Correlations Heatmap ──────────────────────────────────────────────
section_title("📈 Inter-Feature Correlation Heatmap")
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
corr_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
st.plotly_chart(chart_correlation(df, corr_cols), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Feature Importance Section ────────────────────────────────────────────────
section_title("🧠 Top Predictive Clinical Feature Weights")
if metadata and metadata.get("feature_importance"):
    fig_fi = chart_feature_importance(metadata["feature_importance"])
    if fig_fi is not None:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        method = metadata["feature_importance"].get("method", "weights")
        st.caption(
            f"Extraction method: `{method}` (Derived from the selected `{metadata.get('best_model_name')}` pipeline on test evaluation)."
        )
        st.plotly_chart(fig_fi, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("The selected model architecture does not expose direct linear feature weights.")
else:
    st.info("Feature importance data is unavailable. Run `python3 train_model.py` to populate model metadata.")
