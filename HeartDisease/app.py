"""HeartGuard AI — Home Page (Streamlit Multipage App).

Matches Crimson Medical Design System:
- Dark Blood-Red / Crimson Palette
- Heading: "Heart Disease Detection Using Machine Learning" (with "Machine Learning" in bright red)
- Real Biological Anatomical Heart SVG + Animated ECG Telemetry Monitor
- Red "Start Prediction" Button
- Red-Accented Metric Snapshot Cards
"""

from __future__ import annotations

import streamlit as st

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
    page_title="HeartGuard AI — Heart Disease Detection Using Machine Learning",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
metadata = load_metadata_cached()
render_sidebar("Home")
topbar("HeartGuard AI", metadata)
render_nav_bar("Home")

# ── Hero Section (Split: Heading + CTA on Left, Biological Heart + ECG on Right) ─
hero_col1, hero_col2 = st.columns([1.15, 0.85], gap="large")

with hero_col1:
    st.markdown(
        """
        <div style="padding: 0.6rem 0 1.2rem;">
          <div style="display:inline-flex; align-items:center; gap:8px; padding:6px 16px; background:rgba(232,0,30,0.14); border:1px solid rgba(232,0,30,0.35); border-radius:9999px; color:#ff6677; font-family:'Inter',sans-serif; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:18px; box-shadow:0 0 18px rgba(232,0,30,0.15);">
            <span style="width:8px; height:8px; border-radius:50%; background:#e8001e; box-shadow:0 0 10px #e8001e; display:inline-block;"></span>
            Machine Learning • Healthcare
          </div>

          <h1 style="font-family:'Inter',sans-serif; font-size:2.85rem; font-weight:900; color:#ffffff; line-height:1.15; margin:0 0 18px 0; letter-spacing:-0.035em;">
            Heart Disease Detection<br>
            Using <span style="background: linear-gradient(135deg, #ff1a33 0%, #ff8090 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 20px rgba(232,0,30,0.6));">Machine Learning</span>
          </h1>

          <p style="font-size:1.06rem; color:rgba(255,255,255,0.7); margin:0 0 1.8rem 0; line-height:1.65; max-width:580px;">
            Analyze clinical patient attributes and generate an objective, machine-learning-based risk stratification for cardiovascular disease. Built on the validated UCI Cleveland clinical cohort with zero data leakage.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta_col1, cta_col2 = st.columns([1, 1])
    with cta_col1:
        st.page_link(
            "pages/1_Prediction.py",
            label="Start Prediction",
            icon="🫀",
            use_container_width=True,
        )
    with cta_col2:
        st.page_link(
            "pages/3_Model_Performance.py",
            label="View Benchmark",
            icon="📈",
            use_container_width=True,
        )

with hero_col2:
    st.markdown(
        """
        <div class="glass-panel" style="padding: 1.4rem; position:relative; overflow:hidden; border-radius:24px; border:1px solid rgba(232,0,30,0.3); box-shadow:0 20px 50px rgba(0,0,0,0.6), 0 0 35px rgba(232,0,30,0.18);">
          <!-- Glowing background orb -->
          <div style="position:absolute; top:-40px; right:-40px; width:160px; height:160px; border-radius:50%; background:radial-gradient(circle, rgba(232,0,30,0.25) 0%, transparent 70%); pointer-events:none;"></div>

          <!-- Telemetry Header -->
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.08);">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="background:rgba(232,0,30,0.22); color:#ff6677; border:1px solid rgba(232,0,30,0.35); padding:2px 8px; border-radius:6px; font-family:'Inter',sans-serif; font-size:0.7rem; font-weight:700;">LEAD II</span>
              <span style="font-size:0.75rem; color:rgba(255,255,255,0.6);">Real-Time Telemetry</span>
            </div>
            <div style="text-align:right;">
              <span style="font-family:'Inter',sans-serif; font-size:1.5rem; font-weight:900; color:#ff4455; text-shadow:0 0 14px rgba(255,68,85,0.7); line-height:1;">72</span>
              <span style="font-size:0.65rem; color:rgba(255,255,255,0.45); text-transform:uppercase; font-weight:700; display:block;">BPM</span>
            </div>
          </div>

          <!-- Animated ECG Waveform on Dark Grid -->
          <div style="background:#0a0004; border-radius:10px; padding:8px; margin-bottom:12px; border:1px solid rgba(232,0,30,0.25); position:relative; overflow:hidden;">
            <div style="position:absolute; inset:0; background-image:linear-gradient(to right, rgba(232,0,30,0.06) 1px, transparent 1px), linear-gradient(to bottom, rgba(232,0,30,0.06) 1px, transparent 1px); background-size:16px 16px; pointer-events:none;"></div>
            <svg viewBox="0 0 500 80" style="width:100%; height:55px; display:block;" preserveAspectRatio="none">
              <path class="ecg-anim-path" d="M 0,40 L 60,40 L 80,38 L 90,42 L 100,40 L 120,40 L 130,25 L 140,65 L 150,5 L 165,75 L 175,40 L 195,40 L 210,32 L 230,40 L 310,40 L 330,38 L 340,42 L 350,40 L 370,40 L 380,25 L 390,65 L 400,5 L 415,75 L 425,40 L 445,40 L 460,32 L 480,40 L 500,40"
                    fill="none" stroke="#ff1a33" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"
                    style="filter:drop-shadow(0 0 6px rgba(255,26,51,0.85));"/>
            </svg>
          </div>

          <!-- Biometric Readouts Strip -->
          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;">
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:6px 8px;">
              <div style="font-size:0.62rem; color:rgba(255,255,255,0.5); text-transform:uppercase; font-weight:600;">Resting BP</div>
              <div style="font-family:'Inter',sans-serif; font-size:0.92rem; font-weight:700; color:#ffffff;">120 <span style="font-size:0.65rem; color:#ff6677;">mmHg</span></div>
            </div>
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:6px 8px;">
              <div style="font-size:0.62rem; color:rgba(255,255,255,0.5); text-transform:uppercase; font-weight:600;">Cholesterol</div>
              <div style="font-family:'Inter',sans-serif; font-size:0.92rem; font-weight:700; color:#ffffff;">195 <span style="font-size:0.65rem; color:#ff6677;">mg/dl</span></div>
            </div>
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:6px 8px;">
              <div style="font-size:0.62rem; color:rgba(255,255,255,0.5); text-transform:uppercase; font-weight:600;">ST Segment</div>
              <div style="font-family:'Inter',sans-serif; font-size:0.92rem; font-weight:700; color:#ffffff;">Normal <span style="font-size:0.65rem; color:#ff6677;">0.0mm</span></div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Red-Accented Metric Snapshot Cards at the Bottom of Hero ─────────────────
if metadata is None:
    st.warning("Model artifacts not found. Run `python3 train_model.py` to train and evaluate the pipeline.")
else:
    best_model = metadata["best_model_name"]
    bm = metadata["model_comparison"][best_model]
    n_rows, n_cols = metadata["dataset_shape"]

    section_title("Engine Performance Snapshot")
    stat_grid(
        stat_card("🎯", "Sensitivity / Recall", f"{bm['recall'] * 100:.1f}%", "Screening priority metric"),
        stat_card("📈", "Test ROC-AUC", f"{bm['roc_auc']:.4f}", "Held-out test set"),
        stat_card("🤖", "Selected Engine", best_model, "Optimized for Recall & AUC"),
        stat_card("🗄️", "Cleveland Patients", f"{n_rows} × {n_cols}", "Patients × clinical features"),
    )

# ── Clinical Medical Disclaimer ───────────────────────────────────────────────
disclaimer_card("home")

# ── Clinical & Pipeline Overview Panels ────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown(
        """
        <div class="glass-panel" style="height:100%;">
          <div style="font-family:'Inter',sans-serif; font-size:1.15rem; font-weight:800; color:#ffffff; margin-bottom:0.6rem; display:flex; align-items:center; gap:8px;">
            <span>🫀</span> Understanding Cardiovascular Risk
          </div>
          <p style="font-size:0.9rem; color:rgba(255,255,255,0.72); line-height:1.6; margin:0;">
            Cardiovascular diseases (CVDs) remain the leading global cause of mortality. Modifiable markers—including resting blood pressure, serum cholesterol, fasting glycemia, and exercise-induced angina—interact dynamically with non-modifiable factors like age and biological sex. Early risk stratification allows for timely lifestyle modifications and preventive clinical follow-up before adverse events occur.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="glass-panel" style="height:100%;">
          <div style="font-family:'Inter',sans-serif; font-size:1.15rem; font-weight:800; color:#ffffff; margin-bottom:0.6rem; display:flex; align-items:center; gap:8px;">
            <span>⚙️</span> ML Pipeline Architecture
          </div>
          <p style="font-size:0.9rem; color:rgba(255,255,255,0.72); line-height:1.6; margin:0;">
            <strong>1. Dataset:</strong> Validated UCI Cleveland cohort (13 physiological attributes).<br>
            <strong>2. Preprocessing:</strong> Stratified 80/20 partition; pipeline median/mode imputation and scaling on training folds only (zero leakage).<br>
            <strong>3. Cross-Validation:</strong> 5-Fold Stratified CV tuning across 7 candidate classifiers.<br>
            <strong>4. Serving:</strong> Strictly decoupled offline training with fast, deterministic serving.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Platform Capabilities & Page Directory ────────────────────────────────────
section_title("Platform Capabilities & Page Directory")
st.markdown(
    """
    <div class="glass-panel" style="margin-bottom: 1rem;">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:20px;">
        <div>
          <div style="font-weight:700; color:#ff4455; font-size:1rem; margin-bottom:6px; display:flex; align-items:center; gap:6px;">
            <span>🔍</span> Biometric Risk Prediction
          </div>
          <div style="font-size:0.86rem; color:rgba(255,255,255,0.68); line-height:1.5;">Validated 13-feature input form with strict range bounds and instant probabilistic classification.</div>
        </div>
        <div>
          <div style="font-weight:700; color:#ff4455; font-size:1rem; margin-bottom:6px; display:flex; align-items:center; gap:6px;">
            <span>📋</span> Clinical Assessment Reports
          </div>
          <div style="font-size:0.86rem; color:rgba(255,255,255,0.68); line-height:1.5;">Rule-based risk factor highlights, tailored lifestyle guidance, and downloadable PDF patient summaries.</div>
        </div>
        <div>
          <div style="font-weight:700; color:#ff4455; font-size:1rem; margin-bottom:6px; display:flex; align-items:center; gap:6px;">
            <span>📊</span> Exploratory Data Insights
          </div>
          <div style="font-size:0.86rem; color:rgba(255,255,255,0.68); line-height:1.5;">Interactive distribution charts, correlation heatmaps, and target-stratified biometric breakdowns.</div>
        </div>
        <div>
          <div style="font-weight:700; color:#ff4455; font-size:1rem; margin-bottom:6px; display:flex; align-items:center; gap:6px;">
            <span>📈</span> Multi-Model Performance
          </div>
          <div style="font-size:0.86rem; color:rgba(255,255,255,0.68); line-height:1.5;">Transparent benchmark comparing Accuracy, Precision, Recall, F1, and ROC curves across 7 algorithms.</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

cap_col1, cap_col2, cap_col3, cap_col4 = st.columns(4)
with cap_col1:
    st.page_link("pages/1_Prediction.py", label="Open Prediction Studio", icon="🔍", use_container_width=True)
with cap_col2:
    st.page_link("pages/2_Data_Analysis.py", label="Explore Data Analytics", icon="📊", use_container_width=True)
with cap_col3:
    st.page_link("pages/3_Model_Performance.py", label="View Benchmark Curves", icon="📈", use_container_width=True)
with cap_col4:
    st.page_link("pages/4_About.py", label="About Team & Scope", icon="ℹ️", use_container_width=True)

st.markdown("---")
st.caption(
    "HeartGuard AI · Pimpri Chinchwad College of Engineering, Pune — Department of CSE · "
    "Supervised by Ms. Suvarna Patil · B.Tech 2nd Year Project · Educational and Research Tool."
)
