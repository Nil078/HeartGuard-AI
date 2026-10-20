# 🫀 HeartGuard AI — Backend & ML Pipeline Documentation

> **Pimpri Chinchwad College of Engineering, Pune — Department of CSE**
> Supervised by Ms. Suvarna Patil · B.Tech 2nd Year Project · Educational & Research Tool

---

## 📌 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Technology Stack](#3-technology-stack)
4. [Directory Structure](#4-directory-structure)
5. [Dataset](#5-dataset)
6. [ML Pipeline — Training (`train_model.py`)](#6-ml-pipeline--training-train_modelpy)
7. [Preprocessing (`utils/preprocessing.py`)](#7-preprocessing-utilspreprocessingpy)
8. [Model Evaluation & Selection (`utils/model_utils.py`)](#8-model-evaluation--selection-utilsmodel_utilspy)
9. [Clinical Risk Rules (`utils/risk_rules.py`)](#9-clinical-risk-rules-utilsrisk_rulespy)
10. [PDF Report Generator (`utils/report_generator.py`)](#10-pdf-report-generator-utilsreport_generatorpy)
11. [Visualization & Charting (`utils/visualization.py`)](#11-visualization--charting-utilsvisualizationpy)
12. [Input Validation (`utils/validation.py`)](#12-input-validation-utilsvalidationpy)
13. [Streamlit Frontend Architecture](#13-streamlit-frontend-architecture)
14. [Flask REST API Server (`server.py`)](#14-flask-rest-api-server-serverpy)
15. [Data Flow: End-to-End Prediction](#15-data-flow-end-to-end-prediction)
16. [Key Design Decisions](#16-key-design-decisions)
17. [Presentation Talking Points](#17-presentation-talking-points)

---

## 1. Project Overview

HeartGuard AI is a **machine-learning-based cardiovascular risk prediction system** that:

- Accepts **13 clinical patient attributes** (age, sex, chest pain type, blood pressure, cholesterol, etc.)
- Passes them through a **trained scikit-learn pipeline** (preprocessor + classifier)
- Outputs a **binary classification**: "Low Risk" vs "Higher Risk Detected"
- Generates **deterministic clinical risk factor highlights** and **lifestyle suggestions**
- Produces a **downloadable PDF patient report**
- Provides **interactive exploratory data analysis** (EDA) charts
- Benchmarks **7 ML algorithms** with transparent comparison metrics

All training happens **offline** via `train_model.py`. The Streamlit app **never retrains** — it only loads and serves the saved model.

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         OFFLINE TRAINING                           │
│                                                                    │
│  data/heart_disease.csv                                            │
│        │                                                           │
│        ▼                                                           │
│  train_model.py                                                    │
│        │                                                           │
│        ├─ utils/preprocessing.py  (clean, impute, encode, scale)   │
│        ├─ utils/model_utils.py    (evaluate, select best model)    │
│        │                                                           │
│        ▼                                                           │
│  heart_disease_model.pkl    (serialized sklearn Pipeline)          │
│  model_metadata.json        (metrics, curves, feature importance)  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       ONLINE SERVING (Streamlit)                   │
│                                                                    │
│  app.py  ──────────  Home page (Hero, metrics, overview)           │
│  pages/1_Prediction.py  ── Form → model.predict() → result + PDF  │
│  pages/2_Data_Analysis.py ── Interactive Plotly EDA charts         │
│  pages/3_Model_Performance.py ── Benchmark table, ROC, confusion   │
│  pages/4_About.py  ──────── Project info & methodology            │
│                                                                    │
│  utils/styling.py        (Crimson Design System CSS)               │
│  utils/visualization.py  (Plotly chart factories)                  │
│  utils/risk_rules.py     (Deterministic clinical rule engine)      │
│  utils/report_generator.py (fpdf2 PDF generator)                   │
│  utils/validation.py     (Input range & type checking)             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | All backend logic |
| **ML Framework** | scikit-learn ≥ 1.3 | Pipelines, model training, evaluation |
| **Boosting** | XGBoost ≥ 2.0 (optional) | Additional candidate classifier |
| **Data Processing** | pandas ≥ 2.0, numpy ≥ 1.24 | DataFrame operations |
| **Frontend** | Streamlit ≥ 1.32 | Multi-page web UI |
| **Charts** | Plotly ≥ 5.18 | Interactive EDA & performance plots |
| **PDF Generation** | fpdf2 ≥ 2.8 | Patient assessment reports |
| **REST API** | Flask ≥ 3.0 + flask-cors | Alternative JSON API server |
| **Serialization** | joblib ≥ 1.3 | Model persistence (.pkl) |

---

## 4. Directory Structure

```
HeartDisease/
├── app.py                      # Streamlit home page (entry point)
├── train_model.py              # Offline training script (run once)
├── server.py                   # Flask REST API server (alternative)
├── heart_disease_model.pkl     # Trained sklearn Pipeline (binary)
├── model_metadata.json         # All metrics, curves, rationale (62 KB)
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml             # Streamlit theme (dark crimson) + server config
├── data/
│   └── heart_disease.csv       # UCI Cleveland heart disease dataset (303 rows)
├── pages/
│   ├── 1_Prediction.py         # Risk prediction form + assessment results
│   ├── 2_Data_Analysis.py      # Interactive EDA charts
│   ├── 3_Model_Performance.py  # Multi-model benchmark comparison
│   └── 4_About.py              # Project methodology & credits
├── utils/
│   ├── __init__.py
│   ├── preprocessing.py        # Feature definitions, cleaning, encoding, splitting
│   ├── model_utils.py          # Model loading, evaluation, selection logic
│   ├── risk_rules.py           # Deterministic clinical risk factor rules
│   ├── report_generator.py     # PDF report generation (fpdf2)
│   ├── validation.py           # Input range validation
│   ├── styling.py              # Crimson Design System (colors, CSS, components)
│   └── visualization.py        # Plotly chart helpers + Streamlit wrappers
└── static/                     # Assets for Flask server (index.html, CSS, JS)
```

---

## 5. Dataset

| Property | Value |
|---|---|
| **Source** | UCI Machine Learning Repository — Cleveland Heart Disease |
| **File** | `data/heart_disease.csv` |
| **Rows** | 303 patients |
| **Features** | 13 clinical attributes + 1 target |
| **Target** | `target` — 0 = No disease, 1–4 = Disease (binarized to 0/1) |

### Feature Descriptions

| # | Feature | Type | Description |
|---|---|---|---|
| 1 | `age` | Numeric | Age in years |
| 2 | `sex` | Categorical | 0 = Female, 1 = Male |
| 3 | `cp` | Categorical | Chest pain type (0–3: typical angina, atypical, non-anginal, asymptomatic) |
| 4 | `trestbps` | Numeric | Resting blood pressure (mm Hg) |
| 5 | `chol` | Numeric | Serum cholesterol (mg/dl) |
| 6 | `fbs` | Categorical | Fasting blood sugar > 120 mg/dl (0/1) |
| 7 | `restecg` | Categorical | Resting ECG results (0–2) |
| 8 | `thalach` | Numeric | Maximum heart rate achieved (bpm) |
| 9 | `exang` | Categorical | Exercise-induced angina (0/1) |
| 10 | `oldpeak` | Numeric | ST depression induced by exercise relative to rest |
| 11 | `slope` | Categorical | Slope of peak exercise ST segment (0–2) |
| 12 | `ca` | Numeric | Number of major vessels colored by fluoroscopy (0–3) |
| 13 | `thal` | Categorical | Thalassemia perfusion scan (1 = fixed defect, 2 = normal, 3 = reversible defect) |

---

## 6. ML Pipeline — Training (`train_model.py`)

### What It Does

This is the **offline training script** — you run it **once** to generate the model artifacts. The Streamlit app never calls `.fit()`.

### Step-by-Step Flow

```
1. Load raw CSV              →  load_raw_dataset()
2. Run diagnostics           →  dataset_diagnostics()
3. Clean data                →  clean_dataset()
     ├─ Remove BOM from column headers
     ├─ Drop duplicate rows
     ├─ Set out-of-range ca values (not 0–3) to NaN
     └─ Set unknown thal values (not 1/2/3) to NaN
4. Split features/target     →  split_xy()
5. Binarize target           →  binarize_target()  (0 vs >0)
6. Train/Test split          →  80% train / 20% test (stratified)
7. For each of 7 candidate models:
     ├─ Build Pipeline: [Preprocessor → Model]
     ├─ GridSearchCV (5-Fold Stratified CV, scoring=roc_auc)
     ├─ Evaluate best on held-out test set
     └─ Extract feature importance (if available)
8. Select best model         →  Weighted score: 35% Recall + 30% AUC + 20% F1 + 15% Acc
9. Save artifacts:
     ├─ heart_disease_model.pkl   (joblib serialized Pipeline)
     └─ model_metadata.json       (all metrics, curves, rationale)
```

### 7 Candidate Algorithms

| # | Algorithm | Scaling | Hyperparameter Grid |
|---|---|---|---|
| 1 | **Logistic Regression** | Yes | C: [0.1, 1.0, 10.0] |
| 2 | **Decision Tree** | No | max_depth: [3,5,7,None], min_samples_split: [2,5,10] |
| 3 | **Random Forest** | No | n_estimators: [50,100], max_depth: [3,5,7], min_samples_split: [2,5] |
| 4 | **Gradient Boosting** | No | n_estimators: [50,100], learning_rate: [0.05,0.1], max_depth: [2,3] |
| 5 | **SVM (RBF kernel)** | Yes | C: [0.1,1.0,10.0], gamma: [scale] |
| 6 | **K-Nearest Neighbors** | Yes | n_neighbors: [3,5,7,9], weights: [uniform, distance] |
| 7 | **XGBoost** (optional) | No | n_estimators: [50,100], max_depth: [3,5], learning_rate: [0.05,0.1] |

### Model Selection Strategy

The best model is chosen by a **weighted composite score** optimized for clinical screening:

```
Score = 0.35 × Recall + 0.30 × ROC-AUC + 0.20 × F1 + 0.15 × Accuracy
```

**Recall is weighted highest** because in a screening context, missing a positive case (false negative) is more dangerous than a false alarm.

### Output Artifacts

| File | Size | Contents |
|---|---|---|
| `heart_disease_model.pkl` | ~5 KB | Serialized `sklearn.pipeline.Pipeline` (preprocessor + best model) |
| `model_metadata.json` | ~62 KB | All metrics, ROC/PR curves, confusion matrices, feature importances, rationale |

---

## 7. Preprocessing (`utils/preprocessing.py`)

### Responsibilities

1. **Feature Column Definitions** — Single source of truth for numeric vs categorical splits
2. **Feature Encodings** — Human-readable labels → integer codes (used by prediction form)
3. **Data Loading** — `load_raw_dataset()` reads the CSV
4. **Dataset Diagnostics** — Missing values, duplicates, out-of-range values
5. **Cleaning** — Remove duplicates, fix out-of-range `ca`/`thal` values
6. **Target Binarization** — Multi-class Cleveland target (0–4) → binary (0/1)
7. **Preprocessor Construction** — `build_preprocessor()` creates a `ColumnTransformer`:

```
ColumnTransformer:
  ├─ num: Pipeline([SimpleImputer(median), ?StandardScaler])  → for numeric features
  └─ cat: Pipeline([SimpleImputer(most_frequent), OneHotEncoder]) → for categorical features
```

### Zero Data Leakage

- Preprocessor is **inside** the `Pipeline`, which means the `GridSearchCV` fits scalers/imputers only on training folds
- Test set is never seen during training or cross-validation
- The app loads the **entire fitted pipeline** and calls `.predict()` — preprocessor is already baked in

---

## 8. Model Evaluation & Selection (`utils/model_utils.py`)

### Functions

| Function | Purpose |
|---|---|
| `evaluate_model()` | Computes accuracy, precision, recall, F1, ROC-AUC, confusion matrix, ROC curve, PR curve on the test set |
| `extract_feature_importance()` | Gets tree `feature_importances_` or logistic `coef_` and groups them back to original 13 features |
| `select_best_model()` | Applies weighted composite scoring to pick the best model |
| `load_model()` / `load_metadata()` | Load serialized artifacts at app startup |

### Selection Weights

```python
SELECTION_WEIGHTS = {
    "recall": 0.35,    # Screening priority — don't miss sick patients
    "roc_auc": 0.30,   # Overall ranking quality
    "f1": 0.20,        # Balance of precision and recall
    "accuracy": 0.15,  # General correctness
}
```

---

## 9. Clinical Risk Rules (`utils/risk_rules.py`)

This is a **deterministic rule engine** — it does NOT use the ML model. It evaluates submitted clinical values against standard ACC/AHA thresholds.

### Risk Factor Rules (8 rules)

| Rule ID | Condition | Description |
|---|---|---|
| `bp_elevated` | `trestbps >= 140` | Elevated resting blood pressure |
| `chol_high` | `chol >= 240` | High serum cholesterol |
| `fbs_high` | `fbs == 1` | Fasting blood sugar > 120 mg/dl |
| `exang_present` | `exang == 1` | Exercise-induced angina present |
| `thalach_low` | `thalach < (220 - age) × 0.70` | Reduced max heart rate for age |
| `oldpeak_high` | `oldpeak >= 2.0` | Significant ST depression |
| `ca_present` | `ca >= 1` | Vessel involvement on fluoroscopy |
| `thal_defect` | `thal ∈ {1, 3}` | Thalassemia perfusion defect |

### Lifestyle Suggestions

Condition-triggered lifestyle and dietary recommendations are generated deterministically based on the same form data. Examples:
- High BP → DASH diet, reduce sodium
- High cholesterol → Dietary changes, omega-3 fatty acids
- Exercise angina → Supervised cardiac rehab

---

## 10. PDF Report Generator (`utils/report_generator.py`)

- Uses **fpdf2** library (no external fonts required — ASCII/Latin-1 core fonts)
- Generates a clean, structured PDF that **matches the on-screen assessment verbatim**
- Contents include:
  - Patient clinical attributes
  - ML prediction result and probability
  - Risk factor highlights
  - Lifestyle suggestions
  - Medical disclaimer
  - Generation timestamp

---

## 11. Visualization & Charting (`utils/visualization.py`)

### Plotly Charts Used

| Chart | Page | Purpose |
|---|---|---|
| Distribution histograms | Data Analysis | Feature distributions by target class |
| Correlation heatmap | Data Analysis | Feature correlation matrix |
| Boxplots | Data Analysis | Feature ranges by target stratification |
| ROC Curves (overlay) | Model Performance | Compare ROC curves across 7 models |
| Confusion Matrix | Model Performance | Best model confusion matrix heatmap |
| Feature Importance bar | Model Performance | Top features driving predictions |
| Probability gauge | Prediction | Visual probability meter for result |

All charts use the `CLINICAL_PLOTLY_LAYOUT` theme from `styling.py` — dark crimson backgrounds with red accent colors.

---

## 12. Input Validation (`utils/validation.py`)

Validates all 13 input fields with **strict clinical range bounds** before they reach the model:

| Field | Type | Valid Range |
|---|---|---|
| `age` | int | 1–120 |
| `trestbps` | int | 60–220 |
| `chol` | int | 100–600 |
| `thalach` | int | 50–250 |
| `oldpeak` | float | 0.0–7.0 |
| `ca` | int | 0–3 |
| Categoricals | int | Must match valid encoding values |

Returns a list of human-readable error messages if any field is out of range.

---

## 13. Streamlit Frontend Architecture

### Multi-Page Structure

The app uses Streamlit's built-in multi-page routing:

| Page | File | Description |
|---|---|---|
| **Home** | `app.py` | Hero section, ECG monitor, metric cards, overview panels |
| **Prediction** | `pages/1_Prediction.py` | 13-field clinical form → model prediction → risk assessment → PDF download |
| **Data Analysis** | `pages/2_Data_Analysis.py` | Interactive Plotly EDA (distributions, correlations, boxplots) |
| **Model Performance** | `pages/3_Model_Performance.py` | Benchmark comparison table, ROC overlay, confusion matrix, feature importances |
| **About** | `pages/4_About.py` | Methodology, dataset source, limitations, team credits |

### Design System (`utils/styling.py`)

- **Theme**: Dark blood-red / crimson medical palette
- **Colors**: `#0f0004` (canvas), `#1a0008` (surface), `#e8001e` (primary red), `#ffffff` (text)
- **Components**: `glass-panel` (glassmorphism cards), `stat_card`, `section_title`, `topbar`, `render_sidebar`
- **CSS injection**: `load_css()` injects ~800 lines of custom CSS into Streamlit

### Key Streamlit Patterns

```python
# Cached model loading (runs once, never retrains)
@st.cache_resource
def load_model_cached():
    return load_model()

# Cached metadata loading
@st.cache_resource
def load_metadata_cached():
    return load_metadata()
```

---

## 14. Flask REST API Server (`server.py`)

An **alternative serving layer** using Flask (not Streamlit). Provides JSON API endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `GET /` | GET | Serve static `index.html` |
| `GET /api/metadata` | GET | Return model metadata JSON |
| `GET /api/encodings` | GET | Return feature encoding maps |
| `GET /api/dataset-stats` | GET | Return exploratory data statistics |
| `POST /api/predict` | POST | Accept 13 clinical fields, return prediction + probability |
| `POST /api/report/pdf` | POST | Generate and return a downloadable PDF report |

---

## 15. Data Flow: End-to-End Prediction

Here's exactly what happens when a user submits the prediction form:

```
1. USER fills 13 fields on the Streamlit prediction form
                    │
2. validate_inputs(form_data)
   └─ Checks ranges, types, returns errors or passes
                    │
3. form_data_to_dataframe(form_data)
   └─ Creates single-row DataFrame in correct column order
                    │
4. model.predict(df)  +  model.predict_proba(df)
   └─ The Pipeline internally runs:
       a) ColumnTransformer: impute + scale numeric, impute + OHE categorical
       b) Classifier: output class (0/1) + probability [p0, p1]
                    │
5. evaluate_risk_factors(form_data)
   └─ Deterministic rule engine: check 8 clinical thresholds
                    │
6. evaluate_lifestyle_suggestions(form_data)
   └─ Condition-triggered dietary & lifestyle recommendations
                    │
7. render_prediction_result(class, p0, p1, model_name)
   └─ Display risk card, probability bar, risk factors, suggestions
                    │
8. generate_patient_pdf(form_data, result, risk_factors, suggestions)
   └─ Create downloadable PDF report
```

---

## 16. Key Design Decisions

### Why Offline Training + Online Serving?

- **Reproducibility**: Same model artifacts, same results every time
- **Speed**: No training overhead at app startup — model loads in <1 second
- **Safety**: Users can never accidentally trigger retraining
- **Auditability**: `model_metadata.json` records every metric, parameter, and rationale

### Why Recall-Weighted Selection?

In a medical screening context, **false negatives are more dangerous than false positives**. A missed positive case means a patient with potential heart disease gets no follow-up. The 35% recall weight ensures the selected model prioritizes catching true positives.

### Why Both Streamlit and Flask?

- **Streamlit**: Rich interactive UI, ideal for demos and presentations
- **Flask**: Headless JSON API, suitable for integration with other frontends or mobile apps
- Both share the same `utils/` modules — single source of truth

### Zero Data Leakage Guarantee

- Preprocessor (imputer + scaler + encoder) is **inside** the Pipeline
- `GridSearchCV` fits preprocessors on each CV training fold only
- Test set is held out until final evaluation
- No metrics are computed on training data

---

## 17. Presentation Talking Points

### Opening (2 min)

> "HeartGuard AI is a machine-learning-based cardiovascular risk prediction system. It takes 13 clinical attributes from a patient — like blood pressure, cholesterol, and ECG results — and uses a trained ML pipeline to classify them as low risk or higher risk for heart disease."

### Dataset & Problem (2 min)

> "We use the UCI Cleveland Heart Disease dataset — 303 patients with 13 features. The original target has 5 classes (0–4), which we binarize into binary classification: 0 = No disease, 1 = Disease."

### ML Pipeline (3 min)

> "We compare 7 algorithms: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, SVM, KNN, and XGBoost. Each is wrapped in a sklearn Pipeline with a ColumnTransformer that handles imputation, scaling, and one-hot encoding. We use 5-Fold Stratified Cross-Validation with GridSearchCV for hyperparameter tuning."

### Model Selection (1 min)

> "We select the best model using a weighted composite score: 35% Recall, 30% ROC-AUC, 20% F1, 15% Accuracy. Recall is weighted highest because in a screening context, missing a sick patient (false negative) is more dangerous than a false alarm."

### No Data Leakage (1 min)

> "The preprocessor is inside the Pipeline, so scalers and imputers are only fit on training folds during cross-validation. The test set is completely held out until final evaluation. There is zero data leakage."

### Serving Architecture (2 min)

> "Training is offline — run once with `train_model.py`. The app loads the serialized pipeline and only calls `.predict()`. We have two serving options: a rich Streamlit UI for interactive use, and a Flask REST API for headless integration."

### Clinical Features (1 min)

> "Beyond the ML prediction, we have a deterministic rule engine that checks 8 clinical thresholds (ACC/AHA guidelines) and generates personalized lifestyle recommendations. These are not ML outputs — they're transparent, auditable rules."

### Demo Points

1. Show the **prediction form** — enter clinical values and submit
2. Show the **assessment result** — risk card, probability, risk factors
3. Show the **PDF download** — clinical report with all details
4. Show the **Data Analysis page** — interactive EDA charts
5. Show the **Model Performance page** — benchmark table, ROC curves
6. Mention the **crimson design system** — dark medical theme with glassmorphism

---

*Generated for HeartGuard AI · PCCOE Pune · CSE Department*
