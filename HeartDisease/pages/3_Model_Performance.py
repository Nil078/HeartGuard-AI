"""Model Performance Page — Benchmark Evaluation & Validation Summary.

Matches Stitch Screen: "Model Evaluation Summary" (ID: 0702dfbb5dc94ffb9c2c405eaa59f080)
"""

from __future__ import annotations

import pandas as pd
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
from utils.visualization import (
    chart_confusion_matrix,
    chart_feature_importance,
    chart_model_bars,
    chart_pr_overlay,
    chart_roc_overlay,
    load_metadata_cached,
)

st.set_page_config(
    page_title="Model Performance | HeartGuard AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()
metadata = load_metadata_cached()
render_sidebar("Model Performance")
topbar("Model Evaluation Summary", metadata)
render_nav_bar("Model Performance")
disclaimer_card("perf")

if metadata is None:
    st.error("Model metadata not found. Run `python3 train_model.py` first.")
    st.stop()

comparison = metadata["model_comparison"]
best_name = metadata["best_model_name"]
best = comparison[best_name]

# ── Engine Status & Benchmark Snapshot ────────────────────────────────────────
section_title(f"🏆 Best Performing Engine: {best_name}")
stat_grid(
    stat_card("🎯", "Sensitivity / Recall", f"{best['recall']:.4f}", "Screening priority metric", "mint"),
    stat_card("📈", "Test ROC-AUC", f"{best['roc_auc']:.4f}", "Primary ranking metric", "teal"),
    stat_card("⚖️", "F1 Score", f"{best['f1']:.4f}", "Harmonic precision-recall mean", "violet"),
    stat_card("🔬", "Test Accuracy", f"{best['accuracy']:.4f}", "Overall test correctness", "teal"),
    stat_card("🛡️", "Precision", f"{best['precision']:.4f}", "Positive predictive value", "violet"),
)

# ── Validation Metrics Comparison Table (Matching Stitch Table) ───────────────
section_title("📋 Multi-Model Validation Benchmark (Held-Out Test Set)")

rows = []
for name, m in comparison.items():
    is_best_row = (name == best_name)
    rows.append({
        "Model Architecture": f"{'⭐ ' if is_best_row else ''}{name}",
        "Accuracy": m["accuracy"],
        "Precision": m["precision"],
        "Recall (Sensitivity)": m["recall"],
        "F1 Score": m["f1"],
        "ROC-AUC": m["roc_auc"],
    })

table_df = pd.DataFrame(rows).set_index("Model Architecture")

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.dataframe(
    table_df.style.format("{:.4f}").highlight_max(
        axis=0, color="rgba(232, 0, 30, 0.25)"
    ),
    use_container_width=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# ── Diagnostic Performance Charts (ROC, PR Curve & Confusion Matrix) ──────────
c1, c2 = st.columns([7, 5])

with c1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    tab_roc, tab_pr = st.tabs(["📈 ROC Curves Overlay", "🎯 Precision-Recall Curves"])
    with tab_roc:
        st.plotly_chart(chart_roc_overlay(comparison), use_container_width=True)
    with tab_pr:
        fig_pr = chart_pr_overlay(comparison)
        if fig_pr:
            st.plotly_chart(fig_pr, use_container_width=True)
        else:
            st.info("Precision-Recall curve data unavailable.")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_confusion_matrix(best["confusion_matrix"], f"Confusion Matrix ({best_name})"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Model Comparison Bar Charts ───────────────────────────────────────────────
section_title("📊 Algorithm Metric Comparisons")
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_model_bars(comparison, "recall", "Test Sensitivity / Recall by Model"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.plotly_chart(
        chart_model_bars(comparison, "roc_auc", "Test ROC-AUC Score by Model"),
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Feature Importance ────────────────────────────────────────────────────────
if metadata.get("feature_importance"):
    section_title(f"🔍 Predictive Feature Weights ({best_name})")
    fig_fi = chart_feature_importance(metadata["feature_importance"])
    if fig_fi:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.plotly_chart(fig_fi, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Model Selection Rationale ─────────────────────────────────────────────────
section_title("🧠 Algorithmic Selection Rationale")
st.markdown(
    f"""
    <div class="glass-panel" style="border-left: 5px solid #e8001e; padding: 1.2rem 1.4rem;">
      <div style="font-family:'Inter',sans-serif; font-size:1.02rem; font-weight:700; color:#ff4455; margin-bottom:0.4rem;">
        Automated Clinical Optimization Rationale
      </div>
      <p style="font-size:0.92rem; color:rgba(255,255,255,0.88); line-height:1.6; margin:0;">
        {metadata['selection_rationale']}
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if metadata.get("xgboost_omission"):
    st.caption(metadata["xgboost_omission"])
