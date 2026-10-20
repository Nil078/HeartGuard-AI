"""Prediction Page — Risk Prediction Form & Assessment Results.

Matches Stitch Screens:
- "Risk Prediction Form" (ID: cf27a71443db4329b577a94f847002ca)
- "Assessment Results" (ID: 1cfede4927374fb885cbfa1750f00340)
"""

from __future__ import annotations

import streamlit as st

from utils.preprocessing import FEATURE_ENCODINGS, form_data_to_dataframe
from utils.report_generator import FIELD_LABELS, _format_field_value, generate_patient_pdf
from utils.risk_rules import evaluate_lifestyle_suggestions, evaluate_risk_factors
from utils.styling import (
    disclaimer_card,
    load_css,
    render_nav_bar,
    render_sidebar,
    section_title,
    topbar,
)
from utils.validation import validate_inputs
from utils.visualization import (
    load_metadata_cached,
    load_model_cached,
    render_prediction_result,
)

st.set_page_config(
    page_title="Risk Prediction | HeartGuard AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
metadata = load_metadata_cached()
render_sidebar("Prediction")
topbar("Risk Assessment Form", metadata)
render_nav_bar("Prediction")
disclaimer_card("pred-top")

model = load_model_cached()
if model is None or metadata is None:
    st.error("Model artifacts not found. Run `python3 train_model.py` to train the model first.")
    st.stop()

enc = FEATURE_ENCODINGS

# ── Form Sections in Glass Panels ─────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom: 1.2rem;">
      <h2 style="font-family:'Inter',sans-serif; font-size:1.6rem; font-weight:800; color:#ffffff; margin:0 0 4px 0;">
        Patient Biometric Entry
      </h2>
      <p style="font-size:0.92rem; color:rgba(255,255,255,0.7); margin:0;">
        Input standard clinical measurements matching the Cleveland cardiovascular cohort protocol.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Viva / Demonstration Presets Toolbar ──────────────────────────────────────
st.markdown(
    """
    <div style="font-size:0.8rem; font-weight:700; color:#ff6677; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">
      ⚡ Quick Presets for Live Testing & College Viva
    </div>
    """,
    unsafe_allow_html=True,
)
col_pre1, col_pre2, col_pre3 = st.columns([1, 1, 1])
with col_pre1:
    if st.button("✓ Load Low-Risk Profile Preset", use_container_width=True):
        st.session_state["val_age"] = 29
        st.session_state["val_sex"] = "Female"
        st.session_state["val_cp"] = "Typical Angina"
        st.session_state["val_trestbps"] = 110
        st.session_state["val_chol"] = 160
        st.session_state["val_fbs"] = "No"
        st.session_state["val_restecg"] = "Normal"
        st.session_state["val_thalach"] = 175
        st.session_state["val_exang"] = "No"
        st.session_state["val_oldpeak"] = 0.0
        st.session_state["val_slope"] = "Downsloping"
        st.session_state["val_ca"] = 0
        st.session_state["val_thal"] = "Normal"
        st.session_state.pop("assessment_result", None)
        st.rerun()

with col_pre2:
    if st.button("⚠️ Load High-Risk Profile Preset", use_container_width=True):
        st.session_state["val_age"] = 68
        st.session_state["val_sex"] = "Male"
        st.session_state["val_cp"] = "Asymptomatic"
        st.session_state["val_trestbps"] = 170
        st.session_state["val_chol"] = 310
        st.session_state["val_fbs"] = "Yes"
        st.session_state["val_restecg"] = "ST-T Wave Abnormality"
        st.session_state["val_thalach"] = 105
        st.session_state["val_exang"] = "Yes"
        st.session_state["val_oldpeak"] = 3.2
        st.session_state["val_slope"] = "Upsloping"
        st.session_state["val_ca"] = 3
        st.session_state["val_thal"] = "Fixed Defect"
        st.session_state.pop("assessment_result", None)
        st.rerun()

with col_pre3:
    if st.button("↺ Reset to Baseline Reference", use_container_width=True):
        st.session_state["val_age"] = 54
        st.session_state["val_sex"] = "Male"
        st.session_state["val_cp"] = "Typical Angina"
        st.session_state["val_trestbps"] = 130
        st.session_state["val_chol"] = 240
        st.session_state["val_fbs"] = "No"
        st.session_state["val_restecg"] = "Normal"
        st.session_state["val_thalach"] = 150
        st.session_state["val_exang"] = "No"
        st.session_state["val_oldpeak"] = 1.0
        st.session_state["val_slope"] = "Flat"
        st.session_state["val_ca"] = 0
        st.session_state["val_thal"] = "Normal"
        st.session_state.pop("assessment_result", None)
        st.rerun()

st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Section 1: Demographics & Chest Pain
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    section_title("👤 Patient Demographics & Symptom History")
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input(
            "Age (Years)", min_value=1, max_value=120,
            value=st.session_state.get("val_age", 54), step=1,
            help="Patient age in completed years."
        )
    with c2:
        sex_opts = list(enc["sex"].keys())
        sex_default = st.session_state.get("val_sex", "Male")
        sex_idx = sex_opts.index(sex_default) if sex_default in sex_opts else 1
        sex_label = st.selectbox("Biological Sex", sex_opts, index=sex_idx, help="Biological sex at birth.")
    with c3:
        cp_opts = list(enc["cp"].keys())
        cp_default = st.session_state.get("val_cp", "Typical Angina")
        cp_idx = cp_opts.index(cp_default) if cp_default in cp_opts else 0
        cp_label = st.selectbox("Chest Pain Type", cp_opts, index=cp_idx, help="Symptom classification of reported chest discomfort.")
    st.markdown('</div>', unsafe_allow_html=True)

# Section 2: Clinical Measurements
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    section_title("🩸 Resting Hemodynamic & Lipid Profile")
    c1, c2, c3 = st.columns(3)
    with c1:
        trestbps = st.number_input(
            "Resting Blood Pressure (mm Hg)", min_value=60, max_value=260,
            value=st.session_state.get("val_trestbps", 130), step=1,
            help="Resting systolic blood pressure upon clinical admission."
        )
    with c2:
        chol = st.number_input(
            "Serum Cholesterol (mg/dl)", min_value=80, max_value=700,
            value=st.session_state.get("val_chol", 240), step=1,
            help="Total fasting serum cholesterol level."
        )
    with c3:
        fbs_opts = list(enc["fbs"].keys())
        fbs_default = st.session_state.get("val_fbs", "No")
        fbs_idx = fbs_opts.index(fbs_default) if fbs_default in fbs_opts else 0
        fbs_label = st.selectbox("Fasting Blood Sugar > 120 mg/dl", fbs_opts, index=fbs_idx, help="Fasting blood sugar indicator above 120 mg/dl.")
    st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Exercise Testing & Electrocardiography
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    section_title("⚡ Exercise Testing & Electrocardiography")
    c1, c2, c3 = st.columns(3)
    with c1:
        restecg_opts = list(enc["restecg"].keys())
        restecg_default = st.session_state.get("val_restecg", "Normal")
        restecg_idx = restecg_opts.index(restecg_default) if restecg_default in restecg_opts else 0
        restecg_label = st.selectbox("Resting ECG Result", restecg_opts, index=restecg_idx, help="Electrocardiographic findings at rest.")
    with c2:
        thalach = st.number_input(
            "Max Heart Rate Achieved (bpm)", min_value=50, max_value=250,
            value=st.session_state.get("val_thalach", 150), step=1,
            help="Peak heart rate recorded during exercise treadmill test."
        )
    with c3:
        exang_opts = list(enc["exang"].keys())
        exang_default = st.session_state.get("val_exang", "No")
        exang_idx = exang_opts.index(exang_default) if exang_default in exang_opts else 0
        exang_label = st.selectbox("Exercise-Induced Angina", exang_opts, index=exang_idx, help="Occurrence of angina during stress test.")

    c1, c2 = st.columns(2)
    with c1:
        oldpeak = st.number_input(
            "ST Depression (Oldpeak, mm)", min_value=0.0, max_value=10.0,
            value=float(st.session_state.get("val_oldpeak", 1.0)), step=0.1, format="%.1f",
            help="ST depression induced by exercise relative to rest."
        )
    with c2:
        slope_opts = list(enc["slope"].keys())
        slope_default = st.session_state.get("val_slope", "Flat")
        slope_idx = slope_opts.index(slope_default) if slope_default in slope_opts else 1
        slope_label = st.selectbox("Slope of Peak Exercise ST", slope_opts, index=slope_idx, help="Slope of the peak exercise ST segment.")
    st.markdown('</div>', unsafe_allow_html=True)

# Section 4: Advanced Diagnostics (Fluoroscopy & Thalassemia)
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    section_title("🔬 Advanced Diagnostic Indicators")
    c1, c2 = st.columns(2)
    with c1:
        ca_opts = [0, 1, 2, 3]
        ca_default = st.session_state.get("val_ca", 0)
        ca_idx = ca_opts.index(ca_default) if ca_default in ca_opts else 0
        ca = st.selectbox("Major Vessels Colored by Fluoroscopy (0–3)", ca_opts, index=ca_idx, help="Number of major vessels (0-3) identified via fluoroscopy.")
    with c2:
        thal_opts = list(enc["thal"].keys())
        thal_default = st.session_state.get("val_thal", "Normal")
        thal_idx = thal_opts.index(thal_default) if thal_default in thal_opts else 0
        thal_label = st.selectbox("Thalassemia Perfusion Status", thal_opts, index=thal_idx, help="Nuclear cardiology perfusion scan indicator.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Assemble Form Data & Validation ───────────────────────────────────────────
form_data = {
    "age": int(age),
    "sex": enc["sex"][sex_label],
    "cp": enc["cp"][cp_label],
    "trestbps": int(trestbps),
    "chol": int(chol),
    "fbs": enc["fbs"][fbs_label],
    "restecg": enc["restecg"][restecg_label],
    "thalach": int(thalach),
    "exang": enc["exang"][exang_label],
    "oldpeak": float(oldpeak),
    "slope": enc["slope"][slope_label],
    "ca": int(ca),
    "thal": enc["thal"][thal_label],
}

errors = validate_inputs(form_data)
for msg in errors:
    st.error(msg)
if errors:
    st.warning("Please correct the flagged input values before generating an assessment.")

st.markdown("<div style='margin-top: 0.8rem;'>", unsafe_allow_html=True)
clicked = st.button(
    "🔍 Run AI Risk Prediction Assessment",
    type="primary",
    disabled=bool(errors),
    use_container_width=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ── Inference & Assessment Results Display ────────────────────────────────────
if clicked and not errors:
    X = form_data_to_dataframe(form_data)
    pred = int(model.predict(X)[0])
    proba = model.predict_proba(X)[0]
    classes = list(model.classes_)
    proba_map = {int(c): float(p) for c, p in zip(classes, proba)}
    p0 = proba_map.get(0, 0.0)
    p1 = proba_map.get(1, 0.0)

    st.session_state["assessment_result"] = {
        "form_data": form_data,
        "pred": pred,
        "p0": p0,
        "p1": p1,
    }

if "assessment_result" in st.session_state:
    res = st.session_state["assessment_result"]
    form_data = res["form_data"]
    pred = res["pred"]
    p0 = res["p0"]
    p1 = res["p1"]

    section_title("Assessment Results")
    render_prediction_result(
        predicted_class=pred,
        proba_0=p0,
        proba_1=p1,
        model_name=metadata["best_model_name"],
    )

    # ── Rule-Based Risk Factors & Recommendations ─────────────────────────────
    risk_factors = evaluate_risk_factors(form_data)
    lifestyle_suggestions = evaluate_lifestyle_suggestions(form_data)

    st.markdown("---")
    section_title("📋 Clinical Profile & Key Risk Contributors")

    # Patient summary grid
    summary_items_html = ""
    for col, lbl in FIELD_LABELS.items():
        val_display = _format_field_value(col, form_data.get(col, "-"))
        summary_items_html += f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding:5px 0; border-bottom:1px solid rgba(232,0,30,0.18);">
          <span style="font-size:0.78rem; color:rgba(255,255,255,0.65);">{lbl}</span>
          <span style="font-size:0.84rem; font-weight:700; color:#ffffff;">{val_display}</span>
        </div>
        """

    st.markdown(
        f"""
        <div class="glass-panel" style="margin-bottom:1.4rem;">
          <div style="font-family:'Inter',sans-serif; font-size:0.95rem; font-weight:700; color:#ff4455; margin-bottom:0.8rem;">
            Biometric Profile Summary
          </div>
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px 24px;">
            {summary_items_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key Risk Factors
    section_title("Primary Clinical Risk Contributors")
    if not risk_factors:
        st.markdown(
            """
            <div class="hg-risk-pill-grid">
              <div class="hg-neutral-pill">
                <span>✓</span> No elevated clinical risk factors flagged from the submitted biometric parameters.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        pills_html = "".join(
            f'<div class="hg-risk-pill"><span style="font-size:0.9rem;">⚠️</span> {factor}</div>'
            for factor in risk_factors
        )
        st.markdown(f'<div class="hg-risk-pill-grid">{pills_html}</div>', unsafe_allow_html=True)

    # Lifestyle & Dietary Suggestions (Grid matching Stitch Assessment screen)
    section_title("Recommended Clinical & Lifestyle Actions")
    for item in lifestyle_suggestions:
        st.markdown(
            f"""
            <div class="hg-lifestyle-card">
              <div class="hg-lifestyle-title">{item['title']}</div>
              <div class="hg-lifestyle-reason">{item['reason']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Clinical follow-up guidance
    st.markdown(
        """
        <div class="glass-panel" style="border-left: 4px solid #e8001e; margin: 1.2rem 0; padding: 1rem 1.2rem;">
          <strong style="color:#ff6677;">Recommended Clinical Next Steps:</strong>
          <span style="color:rgba(255,255,255,0.85); font-size:0.88rem; margin-left:6px;">
            Consult a cardiologist or primary care physician for diagnostic confirmation; repeat fasting lipid panel and ambulatory blood pressure monitoring, and review structured lifestyle modifications.
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Verbatim Medical Disclaimer
    disclaimer_card("report-footer")

    # PDF Report Download Action
    pdf_bytes = generate_patient_pdf(
        form_data=form_data,
        predicted_class=pred,
        proba_0=p0,
        proba_1=p1,
        model_name=metadata["best_model_name"],
        trained_at=metadata.get("trained_at", ""),
        risk_factors=risk_factors,
        lifestyle_suggestions=lifestyle_suggestions,
    )

    st.download_button(
        label="📥 Download Detailed Patient Assessment Report (PDF)",
        data=pdf_bytes,
        file_name="HeartGuard_Patient_Assessment.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
