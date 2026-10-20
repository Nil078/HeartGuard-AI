"""About Page — Project Overview, Student Team, Dataset & Clinical Scope."""

from __future__ import annotations

import streamlit as st

from utils.model_utils import DISCLAIMER
from utils.styling import (
    disclaimer_card,
    load_css,
    render_nav_bar,
    render_sidebar,
    section_title,
    stat_card,
    stat_grid,
    topbar,
)
from utils.visualization import load_metadata_cached

st.set_page_config(
    page_title="About | HeartGuard AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
metadata = load_metadata_cached()
render_sidebar("About")
topbar("About HeartGuard AI", metadata)
render_nav_bar("About")
disclaimer_card("about")

# ── Project Overview ──────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="glass-panel" style="border-left: 5px solid #e8001e; margin-bottom: 1.4rem;">
      <h2 style="font-family:'Inter',sans-serif; font-size:1.4rem; font-weight:800; color:#ffffff; margin:0 0 6px 0;">
        Clinical Research & Educational Purpose
      </h2>
      <p style="font-size:0.92rem; color:rgba(255,255,255,0.75); line-height:1.6; margin:0;">
        <strong>HeartGuard AI</strong> is an undergraduate 2nd Year research and decision-support project developed at Pimpri Chinchwad College of Engineering (PCCOE), Pune. It benchmarks classical machine-learning algorithms on the public UCI Cleveland heart disease cohort to explore predictive capability, feature attribution, and interactive clinical visualization. It is <strong>strictly an educational research tool</strong> and is not approved as a medical device.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Project Team & Guide ──────────────────────────────────────────────────────
section_title("👥 Project Team & Academic Guidance")
stat_grid(
    stat_card("🎓", "Team Member", "Neel Chourasia", "B.Tech CSE"),
    stat_card("🎓", "Team Member", "Arnav Abhishek", "B.Tech CSE"),
    stat_card("🎓", "Team Member", "Chandan Kumar Malakar", "B.Tech CSE"),
    stat_card("🎓", "Team Member", "Kunal Kumar Mishra", "B.Tech CSE"),
)

st.markdown(
    """
    <div class="glass-panel" style="margin-top: 0.8rem; padding: 1.1rem 1.4rem;">
      <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:1.6rem;">🩺</span>
        <div>
          <div style="font-family:'Inter',sans-serif; font-size:1.05rem; font-weight:700; color:#ff4455;">
            Faculty Guide: Ms. Suvarna Patil
          </div>
          <div style="font-size:0.84rem; color:rgba(255,255,255,0.65);">
            Department of Computer Science & Engineering · Pimpri Chinchwad College of Engineering (PCCOE), Pune
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Dataset Description ───────────────────────────────────────────────────────
section_title("🗄️ Clinical Dataset Specification")
st.markdown(
    """
    <div class="glass-panel">
      <p style="font-size:0.9rem; color:rgba(255,255,255,0.8); line-height:1.55; margin-bottom:12px;">
        Training utilizes the standard <strong>UCI Cleveland Heart Disease dataset</strong> (303 patient records, 13 physiological input features and 1 binary diagnostic outcome).
      </p>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:10px 20px; font-size:0.84rem; color:rgba(255,255,255,0.75);">
        <div><strong style="color:#ffffff;">• Demographics:</strong> Age, Biological Sex</div>
        <div><strong style="color:#ffffff;">• Symptoms:</strong> Chest Pain Type (4 categories)</div>
        <div><strong style="color:#ffffff;">• Hemodynamics:</strong> Resting Blood Pressure, Serum Cholesterol</div>
        <div><strong style="color:#ffffff;">• Glycemia:</strong> Fasting Blood Sugar (&gt; 120 mg/dl)</div>
        <div><strong style="color:#ffffff;">• Electrocardiography:</strong> Resting ECG, ST Slope</div>
        <div><strong style="color:#ffffff;">• Stress Testing:</strong> Peak Heart Rate, Exercise Angina, Oldpeak</div>
        <div><strong style="color:#ffffff;">• Advanced Diagnostics:</strong> Fluoroscopy Vessels, Thalassemia Scan</div>
        <div><strong style="color:#ffffff;">• Outcome:</strong> 0 = No Disease, 1 = Heart Disease</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Preprocessing & Limitations from Metadata ─────────────────────────────────
if metadata:
    section_title("📋 Pipeline Diagnostics & Limitations")
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("<strong style='color:#ffffff;'>Preprocessing & Data Pipeline Log:</strong>", unsafe_allow_html=True)
    for note in metadata.get("preprocessing_report", [metadata.get("preprocessing_notes", "")]):
        if note:
            st.markdown(f"• <span style='color:rgba(255,255,255,0.7); font-size:0.86rem;'>{note}</span>", unsafe_allow_html=True)

    st.markdown("<br><strong style='color:#ffffff;'>Clinical & Dataset Limitations:</strong>", unsafe_allow_html=True)
    for item in metadata.get("limitations", []):
        st.markdown(f"• <span style='color:rgba(255,255,255,0.7); font-size:0.86rem;'>{item}</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Retraining Instructions ───────────────────────────────────────────────────
section_title("🔄 Offline Model Retraining Protocol")
st.code(
    """# Execute offline pipeline to retrain, tune, evaluate, and save artifacts:
python3 train_model.py

# Launch Streamlit interactive dashboard:
streamlit run app.py""",
    language="bash",
)

st.markdown("---")
st.caption(f"Medical Policy: {DISCLAIMER}")
