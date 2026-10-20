# Instructions: HeartGuard AI — Heart Disease Risk Prediction (Streamlit Edition)

**Audience:** Coding agent / developers working in this repo.
**Stack:** Python + scikit-learn + Streamlit + Plotly + fpdf2.

**Team:** Neel Chourasia, Arnav Abhishek, Chandan Kumar Malakar, Kunal Kumar Mishra (B.Tech 2nd Year)  
**Guide:** Ms. Suvarna Patil — Pimpri Chinchwad College of Engineering, Pune — Dept. of CSE

---

## 0. Golden Rules

1. **No hardcoded results.** Every metric, curve, and prediction originates from real evaluations against `data/heart_disease.csv`.
2. **No data leakage.** Stratified 80/20 split before any fitting. Imputers and scalers fit on `X_train` only.
3. **Educational tool, not a diagnosis.** Every prediction surface carries the mandatory medical disclaimer.
4. **Generalization optimization.** Model choice prioritizes test-set Recall, ROC-AUC, F1, and Accuracy.
5. **Train once, serve many times.** `train_model.py` is offline only; app only loads saved artifacts.
6. **Deterministic clinical rules.** Risk factors and lifestyle suggestions are evaluated from submitted values using auditable rule tables in `utils/risk_rules.py`.

---

## 1. Project Structure

```
heart-disease-prediction/
│
├── app.py                         # Home page & Health Overview
├── train_model.py                 # Offline training & evaluation script
├── heart_disease_model.pkl        # Best fitted Pipeline artifact
├── model_metadata.json            # Model parameters, test metrics & curves
├── requirements.txt               # Dependencies
├── README.md
├── instructions.md
│
├── data/
│   └── heart_disease.csv          # UCI Cleveland heart disease dataset
│
├── pages/
│   ├── 1_Prediction.py            # Clinical form, inference, patient report & PDF
│   ├── 2_Data_Analysis.py         # Exploratory data visualizations
│   ├── 3_Model_Performance.py     # Multi-model evaluation & benchmark
│   └── 4_About.py                 # Team, dataset details & limitations
│
└── utils/
    ├── preprocessing.py           # Pipelines, encodings, data loaders
    ├── model_utils.py             # Evaluation helpers & metadata
    ├── validation.py              # Input validation rules
    ├── styling.py                 # Central design system & tokens
    ├── visualization.py           # Dark Plotly chart generators
    ├── risk_rules.py              # Deterministic clinical & lifestyle rules
    └── report_generator.py        # PDF report generator (fpdf2)
```

---

## 2. Definition of Done Checklist

- [x] `pip install -r requirements.txt` installs all dependencies cleanly.
- [x] `python3 train_model.py` runs end-to-end: diagnostics → cleaning → 80/20 stratified split → CV hyperparameter search → test evaluation → writes `heart_disease_model.pkl` and `model_metadata.json` with real numbers.
- [x] `streamlit run app.py` launches without errors; functional sidebar navigation with `st.page_link`.
- [x] Home page displays real metric snapshot cards and model ranking progress bars.
- [x] Prediction page validates all 13 inputs, executes pipeline inference, displays class probabilities and gauge, and renders the Comprehensive Patient Assessment Report.
- [x] Risk-factor and lifestyle rules in `utils/risk_rules.py` are data-driven, auditable, and trace directly to submitted values.
- [x] Downloadable PDF patient report generated via `utils/report_generator.py` matches on-screen report content verbatim.
- [x] Data Analysis page renders all interactive exploratory charts on real dataset.
- [x] Model Performance page displays comparison table, ROC overlay, confusion matrix, and feature importances from real training run.
- [x] No hardcoded metrics, no fabricated accuracy, no data leakage, no fake medical claims.
