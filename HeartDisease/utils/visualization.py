"""Shared Streamlit UI helpers and Plotly charts matching Clinical Clarity design system."""

from __future__ import annotations

from typing import Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.model_utils import DISCLAIMER, load_metadata, load_model
from utils.preprocessing import CATEGORY_DISPLAY, clean_dataset, load_raw_dataset
from utils.styling import (
    AMBER,
    CLINICAL_PLOTLY_LAYOUT,
    ERROR,
    ON_SURFACE,
    ON_SURFACE_VARIANT,
    OUTLINE_VARIANT,
    PRIMARY,
    PRIMARY_CONTAINER,
    RED_SOFT,
    RED_VIVID,
    SECONDARY,
    SURFACE_CONTAINER_HIGHEST,
    TERTIARY_CONTAINER,
    disclaimer_card,
    stat_card,
)

PALETTE = {
    "primary": PRIMARY,
    "teal": PRIMARY_CONTAINER,
    "violet": SECONDARY,
    "low": TERTIARY_CONTAINER,
    "high": ERROR,
    "amber": AMBER,
    "text": ON_SURFACE,
    "muted": ON_SURFACE_VARIANT,
}
PLOTLY_LAYOUT = CLINICAL_PLOTLY_LAYOUT


@st.cache_resource
def load_model_cached():
    return load_model()


@st.cache_resource
def load_metadata_cached():
    return load_metadata()


@st.cache_data
def load_cleaned_dataset():
    raw = load_raw_dataset()
    return clean_dataset(raw)


def inject_css() -> None:
    pass


def render_disclaimer(key: str = "disclaimer") -> None:
    disclaimer_card(key)


def render_metric_card(label: str, value: str, icon: str = "📊", accent: str = "teal") -> None:
    st.markdown(stat_card(icon, label, value, accent=accent), unsafe_allow_html=True)


def render_prediction_result(
    predicted_class: int,
    proba_0: float,
    proba_1: float,
    model_name: str,
) -> None:
    """Render Assessment Results matching the Stitch screen layout."""
    is_high = int(predicted_class) == 1
    risk_label = "Higher Risk Detected" if is_high else "Low Risk Profile"
    badge_icon = "⚠️" if is_high else "✅"
    card_cls = "hg-result-card-high" if is_high else "hg-result-card-low"
    risk_color = ERROR if is_high else TERTIARY_CONTAINER
    risk_pct = float(proba_1) * 100.0

    st.markdown(
        f"""
        <div class="{card_cls}">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
            <div>
              <div style="display:inline-flex; align-items:center; gap:6px; padding:4px 14px; background:{'rgba(186,26,26,0.12)' if is_high else 'rgba(0,131,86,0.12)'}; border:1px solid {'rgba(186,26,26,0.35)' if is_high else 'rgba(0,131,86,0.35)'}; border-radius:9999px; color:{risk_color}; font-family:'Inter',sans-serif; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
                <span>{badge_icon}</span> {risk_label}
              </div>
              <h2 style="font-family:'Inter',sans-serif; font-size:1.75rem; font-weight:800; color:{ON_SURFACE}; margin:0 0 6px 0; letter-spacing:-0.02em;">
                {'Elevated Cardiovascular Risk' if is_high else 'Optimal / Low Cardiovascular Risk'}
              </h2>
              <p style="font-size:0.92rem; color:{ON_SURFACE_VARIANT}; margin:0 0 12px 0; max-width:640px; line-height:1.5;">
                {'Based on the entered biometric parameters, the ML model indicates an elevated likelihood of cardiovascular concern. Clinical consultation and periodic monitoring are recommended.' if is_high else 'Based on the entered biometric parameters, the ML model indicates a favorable baseline profile with low probability of significant cardiovascular concern.'}
              </p>
              <div style="font-size:0.8rem; color:{ON_SURFACE_VARIANT};">
                Engine: <strong style="color:{PRIMARY};">{model_name}</strong> &nbsp;·&nbsp;
                P(No Disease): <strong style="color:{ON_SURFACE};">{proba_0:.4f}</strong> &nbsp;·&nbsp;
                P(Heart Disease): <strong style="color:{ON_SURFACE};">{proba_1:.4f}</strong>
              </div>
            </div>
            <div style="text-align:center; min-width:140px; background:rgba(0,0,0,0.45); border:1px solid rgba(232,0,30,0.35); border-radius:18px; padding:12px 20px; box-shadow:0 8px 24px rgba(0,0,0,0.5);">
              <div style="font-family:'Inter',sans-serif; font-size:2.2rem; font-weight:900; color:{risk_color}; line-height:1; text-shadow:0 0 16px {risk_color};">
                {risk_pct:.1f}%
              </div>
              <div style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; color:rgba(255,255,255,0.7); font-weight:700; margin-top:4px;">
                Risk Score
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Circular Gauge Plot
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            number={"suffix": "%", "valueformat": ".2f", "font": {"color": risk_color, "size": 32, "family": "Inter"}},
            title={"text": "Estimated Probability of Cardiovascular Event (P(Class 1))", "font": {"color": "#ffffff", "size": 13, "family": "Inter"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.6)", "tickfont": {"color": "rgba(255,255,255,0.6)", "size": 10}},
                "bar": {"color": risk_color, "thickness": 0.28},
                "bgcolor": "rgba(255,255,255,0.06)",
                "bordercolor": "rgba(232, 0, 30, 0.3)",
                "steps": [
                    {"range": [0, 50], "color": "rgba(5, 150, 105, 0.2)"},
                    {"range": [50, 100], "color": "rgba(232, 0, 30, 0.2)"},
                ],
                "threshold": {
                    "line": {"color": AMBER, "width": 3},
                    "thickness": 0.8,
                    "value": 50,
                },
            },
        )
    )
    fig_gauge.update_layout(
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, Open Sans, sans-serif", "color": "#ffffff"},
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)


def apply_category_labels(series: pd.Series, column: str) -> pd.Series:
    mapping = CATEGORY_DISPLAY.get(column, {})
    return series.map(lambda v: mapping.get(int(v), str(v)) if pd.notna(v) else "Missing")


# ── Chart Builders ────────────────────────────────────────────────────────────

def chart_class_balance(df: pd.DataFrame) -> go.Figure:
    counts = df["target"].value_counts().sort_index()
    labels = counts.index.map(lambda v: "Heart Disease (1)" if int(v) == 1 else "No Heart Disease (0)")
    fig = px.bar(
        x=list(labels),
        y=counts.values,
        labels={"x": "Class", "y": "Count"},
        title="Target Class Balance",
        color=list(labels),
        color_discrete_map={
            "No Heart Disease (0)": TERTIARY_CONTAINER,
            "Heart Disease (1)": ERROR,
        },
    )
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig.update_traces(marker_line_width=1, marker_line_color="rgba(255,255,255,0.8)")
    return fig


def chart_histogram(df: pd.DataFrame, column: str, title: str, xaxis: str) -> go.Figure:
    fig = px.histogram(
        df,
        x=column,
        nbins=25,
        title=title,
        labels={column: xaxis, "count": "Frequency"},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_traces(marker_line_width=1, marker_line_color="rgba(255,255,255,0.8)")
    return fig


def chart_by_target(df: pd.DataFrame, column: str, title: str, kind: str = "box") -> go.Figure:
    plot_df = df.copy()
    plot_df["Heart Disease"] = plot_df["target"].map({0: "No", 1: "Yes"})
    if kind == "box":
        fig = px.box(
            plot_df,
            x="Heart Disease",
            y=column,
            color="Heart Disease",
            title=title,
            color_discrete_map={"No": TERTIARY_CONTAINER, "Yes": ERROR},
        )
    else:
        if column in CATEGORY_DISPLAY:
            plot_df[column] = apply_category_labels(plot_df[column], column)
        fig = px.histogram(
            plot_df,
            x=column,
            color="Heart Disease",
            barmode="group",
            title=title,
            color_discrete_map={"No": TERTIARY_CONTAINER, "Yes": ERROR},
        )
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


def chart_correlation(df: pd.DataFrame, columns: list[str]) -> go.Figure:
    corr = df[columns].corr(numeric_only=True)
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale=[[0, "#2563eb"], [0.5, "rgba(26, 0, 8, 0.9)"], [1, RED_VIVID]],
        zmin=-1,
        zmax=1,
        title="Clinical Feature Correlation Heatmap",
        aspect="auto",
    )
    fig.update_traces(textfont=dict(color="#ffffff", size=10))
    fig.update_layout(**PLOTLY_LAYOUT, height=540)
    return fig


def chart_feature_importance(importance: dict[str, Any] | None) -> go.Figure | None:
    if not importance or not importance.get("grouped"):
        return None
    grouped = importance["grouped"]
    items = sorted(grouped.items(), key=lambda kv: abs(kv[1]), reverse=True)
    colors = [RED_VIVID if v >= 0 else RED_SOFT for _, v in items]
    fig = px.bar(
        x=[v for _, v in items],
        y=[k for k, _ in items],
        orientation="h",
        title="Top Predictive Feature Weights (Best Model)",
        labels={"x": "Relative Weight / Importance", "y": "Feature"},
        color_discrete_sequence=[RED_VIVID],
    )
    fig.update_traces(marker_color=colors, marker_line_width=1, marker_line_color="rgba(255,255,255,0.4)")
    base = {k: v for k, v in PLOTLY_LAYOUT.items() if k != "yaxis"}
    yaxis_base = PLOTLY_LAYOUT.get("yaxis", {})
    fig.update_layout(**base, yaxis=dict(autorange="reversed", **yaxis_base))
    return fig


def chart_model_bars(comparison: dict[str, dict[str, Any]], metric: str, title: str) -> go.Figure:
    names = list(comparison.keys())
    values = [comparison[n][metric] for n in names]
    bar_colors = [RED_VIVID if v == max(values) else "rgba(165, 0, 52, 0.65)" for v in values]
    fig = go.Figure(
        go.Bar(
            x=names,
            y=values,
            marker=dict(color=bar_colors, line=dict(color="rgba(255, 26, 51, 0.5)", width=1)),
            text=[f"{v:.3f}" for v in values],
            textposition="outside",
            textfont=dict(color="#ffffff", size=11),
        )
    )
    base = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("yaxis", "xaxis")}
    fig.update_layout(
        title=title,
        yaxis=dict(range=[0, 1.1], **CLINICAL_PLOTLY_LAYOUT.get("yaxis", {})),
        xaxis=dict(tickangle=-20, **CLINICAL_PLOTLY_LAYOUT.get("xaxis", {})),
        showlegend=False,
        **base,
    )
    return fig


def chart_roc_overlay(comparison: dict[str, dict[str, Any]]) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[0, 1], y=[0, 1], mode="lines", name="Chance Line",
            line=dict(dash="dash", color="rgba(255,255,255,0.3)", width=1.5),
        )
    )
    series_colors = [RED_VIVID, "#ff4455", TERTIARY_CONTAINER, AMBER, "#ff8090", "#c80028", "#ff1a33"]
    for idx, (name, metrics) in enumerate(comparison.items()):
        roc = metrics.get("roc_curve") or {}
        if not roc.get("fpr"):
            continue
        auc = metrics.get("roc_auc")
        fig.add_trace(
            go.Scatter(
                x=roc["fpr"],
                y=roc["tpr"],
                mode="lines",
                name=f"{name} (AUC={auc:.3f})" if auc is not None else name,
                line=dict(color=series_colors[idx % len(series_colors)], width=2.2),
            )
        )
    fig.update_layout(
        title="Test-Set ROC Curves (Multi-Model Comparison)",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        **PLOTLY_LAYOUT,
        height=480,
    )
    return fig


def chart_confusion_matrix(cm: list[list[int]], title: str) -> go.Figure:
    fig = px.imshow(
        cm,
        text_auto=True,
        color_continuous_scale=[[0, "rgba(26, 0, 8, 0.8)"], [0.5, "#a50034"], [1, RED_VIVID]],
        labels=dict(x="Predicted Class", y="Actual Class", color="Sample Count"),
        x=["No Disease (0)", "Heart Disease (1)"],
        y=["No Disease (0)", "Heart Disease (1)"],
        title=title,
    )
    fig.update_traces(textfont=dict(color="#ffffff", size=16))
    fig.update_layout(**PLOTLY_LAYOUT, height=400, coloraxis_showscale=False)
    return fig


def chart_pr_overlay(comparison: dict[str, dict[str, Any]]) -> go.Figure:
    """Render Precision-Recall curves across candidate models."""
    fig = go.Figure()
    series_colors = [RED_VIVID, "#ff4455", TERTIARY_CONTAINER, AMBER, "#ff8090", "#c80028", "#ff1a33"]
    for idx, (name, metrics) in enumerate(comparison.items()):
        pr = metrics.get("pr_curve") or {}
        if not pr.get("recall"):
            continue
        fig.add_trace(
            go.Scatter(
                x=pr["recall"],
                y=pr["precision"],
                mode="lines",
                name=f"{name} (F1={metrics.get('f1', 0):.3f})",
                line=dict(color=series_colors[idx % len(series_colors)], width=2.2),
            )
        )
    fig.update_layout(
        title="Test-Set Precision-Recall Curves (Screening Evaluation)",
        xaxis_title="Recall / Sensitivity",
        yaxis_title="Precision / Positive Predictive Value",
        **PLOTLY_LAYOUT,
        height=480,
    )
    return fig
