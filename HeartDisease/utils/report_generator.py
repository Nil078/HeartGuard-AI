"""PDF Report Generator for HeartGuard AI Patient Assessments.

Generates a clean, structured PDF report matching the on-screen assessment
verbatim. Uses fpdf2 with clean ASCII/Latin-1 core font compatibility.
Pure function, no Streamlit dependencies. Styled with the website's
rich Crimson/Cherry Medical design palette.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from fpdf import FPDF

from utils.model_utils import DISCLAIMER
from utils.preprocessing import CATEGORY_DISPLAY

FIELD_LABELS: dict[str, str] = {
    "age": "Age",
    "sex": "Sex",
    "cp": "Chest Pain Type",
    "trestbps": "Resting Blood Pressure",
    "chol": "Serum Cholesterol",
    "fbs": "Fasting Blood Sugar",
    "restecg": "Resting ECG",
    "thalach": "Max Heart Rate",
    "exang": "Exercise Angina",
    "oldpeak": "Oldpeak (ST Depression)",
    "slope": "ST Slope",
    "ca": "Major Vessels (0-3)",
    "thal": "Thalassemia",
}

FIELD_UNITS: dict[str, str] = {
    "age": "years",
    "trestbps": "mm Hg",
    "chol": "mg/dl",
    "thalach": "bpm",
    "oldpeak": "mm",
}


def _clean_text(text: str) -> str:
    """Normalize unicode dashes, quotes, and symbols to standard ASCII."""
    replacements = {
        "—": " - ",
        "–": "-",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "≥": ">=",
        "≤": "<=",
        "•": "*",
        "✓": "[OK]",
        "⚠️": "[!]",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text


def _format_field_value(col: str, val: Any) -> str:
    """Format raw value into human readable string with units or label."""
    if col in CATEGORY_DISPLAY and int(val) in CATEGORY_DISPLAY[col]:
        return _clean_text(str(CATEGORY_DISPLAY[col][int(val)]))
    unit = FIELD_UNITS.get(col, "")
    return _clean_text(f"{val} {unit}".strip())


class PatientReportPDF(FPDF):
    def header(self):
        # ── Crimson / Burgundy Header Banner ──
        self.set_fill_color(26, 0, 8)  # Deep Burgundy #1a0008
        self.rect(0, 0, 210, 22, "F")

        # ── Vivid Red Accent Stripe ──
        self.set_fill_color(232, 0, 30)  # Primary Vivid Red #e8001e
        self.rect(0, 21.2, 210, 0.8, "F")

        # HeartGuard AI Logo (if available)
        logo_path = Path(__file__).resolve().parent.parent / "stitch_screens" / "2_heartguard_ai_logo.png"
        if logo_path.exists():
            try:
                self.image(str(logo_path), x=12, y=4.5, w=13, h=13)
                tx = 29
            except Exception:
                tx = 12
        else:
            tx = 12

        # Title: HeartGuard AI - Patient Assessment Report
        self.set_xy(tx, 5)
        self.set_font("Helvetica", "B", 12.5)
        self.set_text_color(255, 255, 255)
        self.cell(33, 6, "HeartGuard AI", ln=0)
        self.set_text_color(255, 102, 119)  # Coral / Cherry Accent #ff6677
        self.cell(0, 6, "- Patient Assessment Report", ln=1)

        # Subtitle: Clinical Decision Support
        self.set_xy(tx, 11)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(255, 204, 212)
        self.cell(0, 5, "Cardiovascular Risk Screening & Decision Support", ln=0)

        # Top Right Badge
        self.set_xy(130, 7.5)
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(255, 102, 119)
        self.cell(68, 6, "CLINICAL TELEMETRY", align="R", ln=1)
        self.ln(12)

    def footer(self):
        # Footer dividing line in cherry red
        self.set_draw_color(232, 0, 30)
        self.set_line_width(0.3)
        self.line(12, 283, 198, 283)

        self.set_y(-13)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(140, 100, 110)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        self.cell(
            0, 5,
            f"Generated: {ts} | HeartGuard AI - PCCOE Department of CSE | Educational & Research Use Only",
            align="C",
        )


def generate_patient_pdf(
    form_data: dict[str, Any],
    predicted_class: int,
    proba_0: float,
    proba_1: float,
    model_name: str,
    trained_at: str,
    risk_factors: list[str],
    lifestyle_suggestions: list[dict[str, str]],
) -> bytes:
    """Generate a clean PDF report matching the on-screen patient assessment."""
    pdf = PatientReportPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(12, 26, 12)
    pdf.set_y(26)

    # ── Section 1: Assessment Outcome & Risk Classification ──────────────────
    is_high = int(predicted_class) == 1
    risk_label = "HIGHER RISK DETECTED" if is_high else "LOW RISK"
    risk_pct = float(proba_1) * 100.0

    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(165, 0, 52)  # Crimson 500
    pdf.cell(0, 7, "1. PREDICTION & RISK ESTIMATION", ln=True)

    # Result Box
    if is_high:
        pdf.set_fill_color(255, 241, 244)  # Soft Rose
        pdf.set_draw_color(232, 0, 30)     # Vivid Cherry Red
        text_label_color = (190, 0, 35)
    else:
        pdf.set_fill_color(246, 253, 249)  # Soft Mint White
        pdf.set_draw_color(5, 150, 105)     # Clinical Emerald Green
        text_label_color = (5, 150, 105)

    pdf.set_line_width(0.6)
    pdf.rect(12, pdf.get_y(), 186, 18, "DF")
    pdf.set_xy(16, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*text_label_color)
    pdf.cell(90, 6, f"Classification: {risk_label}", ln=False)

    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(165, 0, 52)  # Cherry Red Probability
    pdf.cell(90, 6, f"Estimated Risk Probability: {risk_pct:.2f}%", align="R", ln=True)

    pdf.set_xy(16, pdf.get_y() + 1)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(90, 75, 80)
    pdf.cell(
        0, 5,
        f"Model: {_clean_text(model_name)} | P(Class 0 - No Disease): {proba_0:.4f} | P(Class 1 - Heart Disease): {proba_1:.4f}",
        ln=True,
    )
    pdf.ln(4)

    # ── Section 2: Clinical Input Values ──────────────────────────────────────
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(165, 0, 52)
    pdf.cell(0, 7, "2. SUBMITTED CLINICAL VALUES", ln=True)

    # 2-column table for clinical attributes
    pdf.set_font("Helvetica", "", 8)
    cols = list(FIELD_LABELS.keys())
    half = (len(cols) + 1) // 2
    left_cols = cols[:half]
    right_cols = cols[half:]

    start_y = pdf.get_y()
    row_height = 5.2

    for i, col in enumerate(left_cols):
        val_str = _format_field_value(col, form_data.get(col, "-"))
        lbl = FIELD_LABELS.get(col, col)
        # Alternate with soft cherry blush
        pdf.set_fill_color(255, 247, 249) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(12, start_y + (i * row_height), 90, row_height, "F")
        pdf.set_xy(14, start_y + (i * row_height))
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(70, 25, 35)
        pdf.cell(48, row_height, lbl, ln=False)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(20, 20, 20)
        pdf.cell(40, row_height, val_str, align="R", ln=False)

    for i, col in enumerate(right_cols):
        val_str = _format_field_value(col, form_data.get(col, "-"))
        lbl = FIELD_LABELS.get(col, col)
        pdf.set_fill_color(255, 247, 249) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(106, start_y + (i * row_height), 92, row_height, "F")
        pdf.set_xy(108, start_y + (i * row_height))
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(70, 25, 35)
        pdf.cell(50, row_height, lbl, ln=False)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(20, 20, 20)
        pdf.cell(40, row_height, val_str, align="R", ln=False)

    pdf.set_y(start_y + (half * row_height) + 3)

    # ── Section 3: Key Clinical Risk Factors ──────────────────────────────────
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(165, 0, 52)
    pdf.cell(0, 7, "3. KEY CLINICAL RISK FACTORS (DETERMINISTIC EVALUATION)", ln=True)

    if not risk_factors:
        pdf.set_font("Helvetica", "I", 8.5)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "No specific clinical risk factors flagged from the submitted parameters.", ln=True)
    else:
        pdf.set_font("Helvetica", "", 8.5)
        for factor in risk_factors:
            cleaned_factor = _clean_text(factor)
            curr_y = pdf.get_y()
            pdf.set_xy(12, curr_y)
            pdf.set_text_color(232, 0, 30)  # Vivid Red bullet
            pdf.cell(5, 5, "-", ln=0)
            pdf.set_text_color(30, 20, 25)
            pdf.set_xy(17, curr_y)
            pdf.multi_cell(179, 5, cleaned_factor)
    pdf.ln(2)

    # ── Section 4: Lifestyle & Dietary Suggestions ────────────────────────────
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(165, 0, 52)
    pdf.cell(0, 7, "4. LIFESTYLE & DIETARY SUGGESTIONS", ln=True)

    for item in lifestyle_suggestions:
        curr_y = pdf.get_y()
        pdf.set_xy(12, curr_y)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(232, 0, 30)  # Vivid Red bullet
        pdf.cell(5, 5, "-", ln=0)
        pdf.set_text_color(165, 0, 52)  # Cherry Title
        pdf.set_xy(17, curr_y)
        pdf.multi_cell(179, 5, _clean_text(item["title"]))
        pdf.set_font("Helvetica", "", 7.8)
        pdf.set_text_color(95, 70, 78)
        pdf.set_x(17)
        pdf.multi_cell(179, 4.2, f"Reason: {_clean_text(item['reason'])}")
        pdf.ln(1.2)

    pdf.ln(2)

    # ── Section 5: Clinical Follow-up Guidance ─────────────────────────────────
    pdf.set_fill_color(255, 245, 247)   # Soft Rose panel
    pdf.set_draw_color(232, 0, 30)      # Cherry border
    pdf.set_line_width(0.4)
    pdf.rect(12, pdf.get_y(), 186, 12, "DF")
    pdf.set_xy(15, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(165, 0, 52)      # Cherry title
    pdf.cell(0, 4, "Recommended Clinical Follow-up:", ln=True)
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(70, 35, 45)
    pdf.set_x(15)
    pdf.cell(
        0, 4,
        "Consult a cardiologist for clinical confirmation; repeat lipid profile and blood pressure monitoring, and review lifestyle factors at follow-up.",
        ln=True,
    )
    pdf.ln(4)

    # ── Section 6: Medical Disclaimer (Verbatim) ──────────────────────────────
    pdf.set_fill_color(254, 242, 245)  # Burgundy-tinted soft panel
    pdf.set_draw_color(190, 0, 35)     # Deep crimson border
    pdf.set_line_width(0.5)
    cur_y = pdf.get_y()
    pdf.rect(12, cur_y, 186, 14, "DF")
    pdf.set_xy(15, cur_y + 1.5)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(190, 0, 35)      # Deep Crimson Title
    pdf.cell(0, 4, "MANDATORY MEDICAL DISCLAIMER:", ln=True)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(90, 35, 48)
    pdf.set_x(15)
    pdf.multi_cell(180, 3.5, _clean_text(DISCLAIMER))

    return bytes(pdf.output())
