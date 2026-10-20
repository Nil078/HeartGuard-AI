# HeartGuard AI — Terminal Execution & Setup Guide

A complete, step-by-step walkthrough to set up, train, and run the **HeartGuard AI** project from your terminal.

---

## 📋 Prerequisites

- **Python 3.10+** installed
- **Terminal** (Bash on Linux/macOS, or PowerShell/Command Prompt on Windows)
- Git (optional, if cloning)

---

## 🚀 Step-by-Step Instructions

### Step 1: Open Terminal & Navigate to the Project Folder

Open your terminal and change directory into the `HeartDisease` folder:

```bash
cd "/home/nile/Downloads/HeartDisease-20261020T094615Z-1-001 (2)/HeartDisease"
```

Or simply launch using the preconfigured startup scripts:
```bash
./run_streamlit.sh    # Starts Streamlit Dashboard on http://localhost:8501
./run_flask.sh        # Starts Flask Web Application on http://localhost:5050
```

---

### Step 2: Activate the Virtual Environment

The project uses a Python virtual environment containing all required packages (`streamlit`, `scikit-learn`, `pandas`, `plotly`, `fpdf2`, etc.).

#### On Linux / macOS:
```bash
source .venv/bin/activate
```

#### On Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

#### On Windows (Command Prompt):
```cmd
.venv\Scripts\activate.bat
```

> **How to verify:** Your terminal prompt will show `(.venv)` at the beginning of the line:
> ```text
> (.venv) pccoe@machine:~/HeartDisease$
> ```

*(Optional)* If you ever need to create a fresh virtual environment from scratch:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 3: Install or Verify Dependencies

Ensure all required libraries are installed:

```bash
pip install -r requirements.txt
```

Packages installed include:
- `streamlit` — Frontend web dashboard framework
- `scikit-learn` — ML model training, pipelines, and metrics
- `pandas` & `numpy` — Data manipulation & numerical operations
- `plotly` — Interactive clinical data visualizations
- `fpdf2` — Medical PDF report generator
- `joblib` — Model persistence and serialization

---

### Step 4: (Optional) Train / Retrain the Machine Learning Model

The trained model artifact (`heart_disease_model.pkl`) and evaluation metadata (`model_metadata.json`) are already generated. If you want to retrain the model from the raw UCI Cleveland dataset:

```bash
python3 train_model.py
```

**What this step does:**
1. Loads raw dataset from `data/heart_disease.csv`
2. Executes dataset diagnostics, duplicate cleanup, and clinical range boundary checks
3. Performs a strict **Stratified 80/20 Train-Test Split** (`random_state=42`) with zero data leakage
4. Fits a full scikit-learn `Pipeline` (imputation + scaling + classifier)
5. Benchmarks 6+ algorithms using 5-Fold Stratified Cross-Validation
6. Selects the optimal model based on **Recall/Sensitivity (0.35 weight)** + **ROC-AUC (0.30 weight)**
7. Outputs evaluation metrics to `model_metadata.json` and serializes `heart_disease_model.pkl`

---

### Step 5: Launch the Streamlit Web Application

Run the Streamlit application:

```bash
streamlit run app.py
```

You will see terminal output similar to:

```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Streamlit will automatically open your default browser. If it doesn't open automatically, hold `Ctrl` and click the **Local URL** or open your browser manually and visit:

👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🌐 Application Navigation Overview

Once the dashboard loads in your browser, you can explore the following pages from the sidebar:

| Page | Description |
|---|---|
| **🏠 Home (`app.py`)** | Hero telemetry, real biological anatomical heart, live animated ECG, and model performance snapshot. |
| **🔍 Prediction (`pages/1_Prediction.py`)** | Interactive 13-feature biometric entry form, instant probabilistic risk scoring, risk factors, lifestyle recommendations, and one-click PDF report download. |
| **📊 Data Analysis (`pages/2_Data_Analysis.py`)** | Exploratory clinical analytics on the 303 Cleveland cohort patients, class distributions, and correlation heatmaps. |
| **📈 Model Performance (`pages/3_Model_Performance.py`)** | Transparent benchmark comparing Sensitivity/Recall, ROC-AUC, F1, Accuracy, and Precision across all evaluated classifiers. |
| **ℹ️ About (`pages/4_About.py`)** | Project overview, PCCOE student development team, faculty supervisor details, and clinical limitations. |

---

## 🛠️ Alternative: Running the Flask REST API Backend

If you also wish to run the standalone Flask backend (which serves the static web assets and REST API endpoints):

```bash
./run_flask.sh
# OR: python3 server.py
```

The Flask server will start at:
👉 **[http://localhost:5050](http://localhost:5050)**

Available API routes:
- `GET /` — Serves static landing page
- `GET /api/metadata` — Model metadata & evaluation metrics
- `GET /api/dataset/stats` — Dataset summary statistics
- `POST /api/predict` — JSON endpoint for biometric prediction
- `POST /api/report/pdf` — Generates and downloads patient PDF report

---

## 🛑 How to Stop the Server

To stop a running Streamlit or Flask server in your terminal:
- Press **`Ctrl + C`** in the terminal window where the app is running.

---

## ❓ Troubleshooting & FAQs

### 1. `ModuleNotFoundError: No module named 'streamlit'`
**Fix:** You forgot to activate the virtual environment. Run:
```bash
source ../.venv/bin/activate
# or
source .venv/bin/activate
```

### 2. `Port 8501 is already in use`
**Fix:** Specify a different port or kill the existing process:
```bash
streamlit run app.py --server.port 8502
```
Or kill the existing process:
```bash
pkill -f "streamlit run"
```

### 3. Model artifacts not found warning
**Fix:** Run the training script to regenerate the model files:
```bash
python3 train_model.py
```

### 4. Hard Refreshing Changes in Browser
If your browser caches the old CSS, force-reload the page:
- **Chrome / Firefox / Edge:** Press `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac).
- In Streamlit, press **`R`** to rerun the app.

---

## ⚖️ Academic & Medical Policy
*HeartGuard AI is an undergraduate capstone educational research tool developed at Pimpri Chinchwad College of Engineering (PCCOE), Pune. It is not an FDA/CE approved diagnostic medical device. Always consult a licensed physician for clinical diagnosis and treatment.*
