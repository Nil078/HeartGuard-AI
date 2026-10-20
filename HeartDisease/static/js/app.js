/**
 * HeartGuard AI — Frontend Application Logic
 * Integrates with Python Flask ML Backend
 */

// ── State & Cache ─────────────────────────────────────────────────────────────
let appState = {
  currentPatientData: null,
  currentPredictionResult: null,
  metadata: null,
  datasetStats: null,
};

// ── DOM Element Cache ─────────────────────────────────────────────────────────
const dom = {
  form: document.getElementById('prediction-form'),
  submitBtn: document.getElementById('submit-prediction-btn'),
  btnText: document.getElementById('btn-text'),
  btnSpinner: document.getElementById('btn-spinner'),
  resultContainer: document.getElementById('result-container'),
  resultCardBox: document.getElementById('result-card-box'),
  resultIconOrb: document.getElementById('result-icon-orb'),
  resultBadgeText: document.getElementById('result-badge-text'),
  resultHeadingText: document.getElementById('result-heading-text'),
  resultScoreNum: document.getElementById('result-score-num'),
  probaLabel0: document.getElementById('proba-label-0'),
  probaLabel1: document.getElementById('proba-label-1'),
  probaBar0: document.getElementById('proba-bar-0'),
  probaBar1: document.getElementById('proba-bar-1'),
  riskFactorsContainer: document.getElementById('risk-factors-container'),
  lifestyleContainer: document.getElementById('lifestyle-suggestions-container'),
  biometricGrid: document.getElementById('biometric-summary-grid'),
  downloadPdfBtn: document.getElementById('download-pdf-btn'),
  benchmarkTableBody: document.getElementById('benchmark-table-body'),
  selectionRationaleText: document.getElementById('selection-rationale-text'),
  toastContainer: document.getElementById('toast-container'),
  liveBpmDisplay: document.getElementById('live-bpm-display'),
  navLinks: document.querySelectorAll('.nav-link'),
};

// ── Presets for College Demo / Viva Mode ───────────────────────────────────────
const PRESETS = {
  // Verified Cleveland Patient (Target 0: No Heart Disease Detected)
  lowRisk: {
    age: 67,
    sex: 1,
    cp: 0,
    trestbps: 160,
    chol: 286,
    fbs: 0,
    restecg: 0,
    thalach: 108,
    exang: 1,
    oldpeak: 1.5,
    slope: 1,
    ca: 3,
    thal: 2,
  },
  // Verified Cleveland Patient (Target 1: Heart Disease Detected)
  highRisk: {
    age: 63,
    sex: 1,
    cp: 3,
    trestbps: 145,
    chol: 233,
    fbs: 1,
    restecg: 0,
    thalach: 150,
    exang: 0,
    oldpeak: 2.3,
    slope: 0,
    ca: 0,
    thal: 1,
  },
  baseline: {
    age: 54,
    sex: 1,
    cp: 0,
    trestbps: 130,
    chol: 240,
    fbs: 0,
    restecg: 0,
    thalach: 150,
    exang: 0,
    oldpeak: 1.0,
    slope: 1,
    ca: 0,
    thal: 2,
  },
};

// ── Label Mappings ────────────────────────────────────────────────────────────
const LABELS = {
  sex: { 0: 'Female', 1: 'Male' },
  cp: { 0: 'Typical Angina', 1: 'Atypical Angina', 2: 'Non-Anginal', 3: 'Asymptomatic' },
  fbs: { 0: '<= 120 mg/dl', 1: '> 120 mg/dl' },
  restecg: { 0: 'Normal', 1: 'ST-T Abnormality', 2: 'LVH' },
  exang: { 0: 'No', 1: 'Yes' },
  slope: { 0: 'Upsloping', 1: 'Flat', 2: 'Downsloping' },
  ca: { 0: '0 Vessels', 1: '1 Vessel', 2: '2 Vessels', 3: '3 Vessels' },
  thal: { 1: 'Fixed Defect', 2: 'Normal Perfusion', 3: 'Reversible Defect' },
};

// ── Initialization ────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initEventListeners();
  initTelemetrySimulation();
  fetchModelMetadata();
  fetchDatasetStats();
  initScrollSpy();
});

// ── Event Listeners ───────────────────────────────────────────────────────────
function initEventListeners() {
  // Preset buttons
  document.getElementById('preset-low-risk')?.addEventListener('click', () => {
    applyPreset(PRESETS.lowRisk);
    showToast('Loaded Low-Risk Clinical Profile Preset', 'info');
  });

  document.getElementById('preset-high-risk')?.addEventListener('click', () => {
    applyPreset(PRESETS.highRisk);
    showToast('Loaded High-Risk Clinical Profile Preset', 'info');
  });

  document.getElementById('preset-reset')?.addEventListener('click', () => {
    applyPreset(PRESETS.baseline);
    dom.resultContainer.style.display = 'none';
    showToast('Form reset to baseline clinical reference', 'info');
  });

  // Form submit
  dom.form.addEventListener('submit', handleFormSubmit);

  // PDF Download
  dom.downloadPdfBtn.addEventListener('click', handlePdfDownload);
}

// ── Form Values Handling ──────────────────────────────────────────────────────
function applyPreset(data) {
  document.getElementById('input-age').value = data.age;
  document.getElementById('select-sex').value = data.sex;
  document.getElementById('select-cp').value = data.cp;
  document.getElementById('input-trestbps').value = data.trestbps;
  document.getElementById('input-chol').value = data.chol;
  document.getElementById('select-fbs').value = data.fbs;
  document.getElementById('select-restecg').value = data.restecg;
  document.getElementById('input-thalach').value = data.thalach;
  document.getElementById('select-exang').value = data.exang;
  document.getElementById('input-oldpeak').value = data.oldpeak;
  document.getElementById('select-slope').value = data.slope;
  document.getElementById('select-ca').value = data.ca;
  document.getElementById('select-thal').value = data.thal;
}

function getFormData() {
  return {
    age: parseInt(document.getElementById('input-age').value, 10),
    sex: parseInt(document.getElementById('select-sex').value, 10),
    cp: parseInt(document.getElementById('select-cp').value, 10),
    trestbps: parseInt(document.getElementById('input-trestbps').value, 10),
    chol: parseInt(document.getElementById('input-chol').value, 10),
    fbs: parseInt(document.getElementById('select-fbs').value, 10),
    restecg: parseInt(document.getElementById('select-restecg').value, 10),
    thalach: parseInt(document.getElementById('input-thalach').value, 10),
    exang: parseInt(document.getElementById('select-exang').value, 10),
    oldpeak: parseFloat(document.getElementById('input-oldpeak').value),
    slope: parseInt(document.getElementById('select-slope').value, 10),
    ca: parseInt(document.getElementById('select-ca').value, 10),
    thal: parseInt(document.getElementById('select-thal').value, 10),
  };
}

// ── Handle Form Submit ────────────────────────────────────────────────────────
async function handleFormSubmit(e) {
  e.preventDefault();

  const formData = getFormData();
  appState.currentPatientData = formData;

  // Set loading state
  dom.submitBtn.disabled = true;
  dom.btnText.textContent = 'Analyzing Clinical Parameters...';
  dom.btnSpinner.style.display = 'inline-block';

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const data = await res.json();

    if (!res.ok) {
      const err = data.validation_errors ? data.validation_errors.join('; ') : (data.error || 'Prediction failed');
      throw new Error(err);
    }

    appState.currentPredictionResult = data;
    renderPredictionResult(data, formData);

    showToast(`Prediction generated successfully (${data.prediction_label})`, 'success');

    // Smooth scroll down to result card
    setTimeout(() => {
      dom.resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 150);

  } catch (err) {
    console.error('Prediction error:', err);
    showToast(`Error: ${err.message}`, 'error');
  } finally {
    dom.submitBtn.disabled = false;
    dom.btnText.textContent = 'Predict Heart Disease';
    dom.btnSpinner.style.display = 'none';
  }
}

// ── Render Prediction Result ──────────────────────────────────────────────────
function renderPredictionResult(result, patientData) {
  dom.resultContainer.style.display = 'block';

  const isHigh = result.is_high_risk;

  // Toggle card state styling
  dom.resultCardBox.className = `result-card ${isHigh ? 'detected' : 'not-detected'}`;

  // Heading & Badge
  dom.resultIconOrb.textContent = isHigh ? '⚠️' : '✓';
  dom.resultBadgeText.textContent = isHigh ? 'Clinical Alert • Elevated Risk' : 'Optimal Profile • Normal Evaluation';
  dom.resultHeadingText.textContent = result.prediction_label;

  // Risk Score Number
  dom.resultScoreNum.textContent = `${result.risk_score_percent}%`;
  dom.resultScoreNum.style.color = isHigh ? '#fca5a5' : '#86efac';

  // Probabilities Bar
  const p0Pct = (result.probability_no_disease * 100).toFixed(1);
  const p1Pct = (result.probability_heart_disease * 100).toFixed(1);

  dom.probaLabel0.textContent = `P(No Heart Disease / Class 0): ${p0Pct}%`;
  dom.probaLabel1.textContent = `P(Heart Disease Detected / Class 1): ${p1Pct}%`;
  dom.probaBar0.style.width = `${p0Pct}%`;
  dom.probaBar1.style.width = `${p1Pct}%`;

  // Render Risk Factors
  dom.riskFactorsContainer.innerHTML = '';
  if (!result.risk_factors || result.risk_factors.length === 0) {
    dom.riskFactorsContainer.innerHTML = `
      <span class="risk-tag optimal">
        <span>✓</span> No elevated clinical risk factors flagged from the submitted biometric parameters.
      </span>
    `;
  } else {
    result.risk_factors.forEach(rf => {
      const tag = document.createElement('span');
      tag.className = 'risk-tag danger';
      tag.innerHTML = `<span>⚠️</span> ${rf}`;
      dom.riskFactorsContainer.appendChild(tag);
    });
  }

  // Render Lifestyle Suggestions
  dom.lifestyleContainer.innerHTML = '';
  if (result.lifestyle_suggestions && result.lifestyle_suggestions.length > 0) {
    result.lifestyle_suggestions.forEach(item => {
      const card = document.createElement('div');
      card.className = 'lifestyle-card';
      card.innerHTML = `
        <div class="lifestyle-title">${item.title}</div>
        <div class="lifestyle-reason">${item.reason}</div>
      `;
      dom.lifestyleContainer.appendChild(card);
    });
  }

  // Render Biometric Summary Grid
  dom.biometricGrid.innerHTML = `
    <div class="summary-item"><span class="summary-label">Age</span><span class="summary-val">${patientData.age} yrs</span></div>
    <div class="summary-item"><span class="summary-label">Sex</span><span class="summary-val">${LABELS.sex[patientData.sex]}</span></div>
    <div class="summary-item"><span class="summary-label">Chest Pain</span><span class="summary-val">${LABELS.cp[patientData.cp]}</span></div>
    <div class="summary-item"><span class="summary-label">Resting BP</span><span class="summary-val">${patientData.trestbps} mm Hg</span></div>
    <div class="summary-item"><span class="summary-label">Cholesterol</span><span class="summary-val">${patientData.chol} mg/dl</span></div>
    <div class="summary-item"><span class="summary-label">Fasting Sugar</span><span class="summary-val">${LABELS.fbs[patientData.fbs]}</span></div>
    <div class="summary-item"><span class="summary-label">Resting ECG</span><span class="summary-val">${LABELS.restecg[patientData.restecg]}</span></div>
    <div class="summary-item"><span class="summary-label">Max Heart Rate</span><span class="summary-val">${patientData.thalach} bpm</span></div>
    <div class="summary-item"><span class="summary-label">Exercise Angina</span><span class="summary-val">${LABELS.exang[patientData.exang]}</span></div>
    <div class="summary-item"><span class="summary-label">Oldpeak</span><span class="summary-val">${patientData.oldpeak.toFixed(1)} mm</span></div>
    <div class="summary-item"><span class="summary-label">ST Slope</span><span class="summary-val">${LABELS.slope[patientData.slope]}</span></div>
    <div class="summary-item"><span class="summary-label">Fluoroscopy (ca)</span><span class="summary-val">${LABELS.ca[patientData.ca]}</span></div>
    <div class="summary-item"><span class="summary-label">Thalassemia</span><span class="summary-val">${LABELS.thal[patientData.thal]}</span></div>
    <div class="summary-item"><span class="summary-label">Active Model</span><span class="summary-val">${result.model_name}</span></div>
  `;
}

// ── Handle PDF Download ───────────────────────────────────────────────────────
async function handlePdfDownload() {
  if (!appState.currentPatientData) {
    showToast('Please run a prediction first before downloading the report.', 'error');
    return;
  }

  dom.downloadPdfBtn.disabled = true;
  const originalHtml = dom.downloadPdfBtn.innerHTML;
  dom.downloadPdfBtn.innerHTML = `
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="spin">
      <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
      <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"></path>
    </svg>
    <span>Generating PDF Document...</span>
  `;

  try {
    const res = await fetch('/api/report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(appState.currentPatientData),
    });

    if (!res.ok) {
      throw new Error('Failed to generate PDF report from server.');
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `HeartGuard_Patient_Assessment_${Date.now()}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();

    showToast('Official Clinical PDF Report downloaded successfully!', 'success');
  } catch (err) {
    console.error('PDF error:', err);
    showToast(`PDF generation failed: ${err.message}`, 'error');
  } finally {
    dom.downloadPdfBtn.disabled = false;
    dom.downloadPdfBtn.innerHTML = originalHtml;
  }
}

// ── Fetch & Populate Model Metadata ───────────────────────────────────────────
async function fetchModelMetadata() {
  try {
    const res = await fetch('/api/metadata');
    if (!res.ok) return;

    const data = await res.json();
    appState.metadata = data;

    const bestModel = data.best_model_name;
    const comparison = data.model_comparison;

    // Populate Benchmark Table
    if (dom.benchmarkTableBody && comparison) {
      dom.benchmarkTableBody.innerHTML = '';

      // Order models with best model first
      const modelNames = Object.keys(comparison).sort((a, b) => {
        if (a === bestModel) return -1;
        if (b === bestModel) return 1;
        return (comparison[b].roc_auc || 0) - (comparison[a].roc_auc || 0);
      });

      modelNames.forEach(name => {
        const m = comparison[name];
        const isBest = name === bestModel;
        const row = document.createElement('tr');
        if (isBest) row.className = 'selected-model-row';

        row.innerHTML = `
          <td>
            <strong>${name}</strong>
            ${isBest ? '<span class="best-badge">★ Selected Engine</span>' : ''}
          </td>
          <td><span class="score-pill">${(m.recall * 100).toFixed(2)}%</span></td>
          <td><span class="score-pill">${m.roc_auc.toFixed(4)}</span></td>
          <td>${m.f1.toFixed(4)}</td>
          <td>${(m.accuracy * 100).toFixed(2)}%</td>
          <td>${(m.precision * 100).toFixed(2)}%</td>
          <td>
            <span style="font-size:0.75rem; font-weight:700; color:${isBest ? 'var(--teal-600)' : 'var(--slate-500)'};">
              ${isBest ? 'Active Serving Pipeline' : 'Evaluated Candidate'}
            </span>
          </td>
        `;
        dom.benchmarkTableBody.appendChild(row);
      });
    }

    // Update Selection Rationale
    if (dom.selectionRationaleText && data.selection_rationale) {
      dom.selectionRationaleText.textContent = data.selection_rationale;
    }

    // Update KPI indicators in Hero
    if (comparison && comparison[bestModel]) {
      const bm = comparison[bestModel];
      const recEl = document.getElementById('kpi-recall');
      const aucEl = document.getElementById('kpi-auc');
      if (recEl) recEl.innerHTML = `${(bm.recall * 100).toFixed(1)}<span>%</span>`;
      if (aucEl) aucEl.textContent = bm.roc_auc.toFixed(4);

      // Update Confusion Matrix
      if (bm.confusion_matrix) {
        const cm = bm.confusion_matrix;
        document.getElementById('cm-tn').textContent = cm[0][0];
        document.getElementById('cm-fp').textContent = cm[0][1];
        document.getElementById('cm-fn').textContent = cm[1][0];
        document.getElementById('cm-tp').textContent = cm[1][1];
      }
    }

  } catch (err) {
    console.warn('Metadata fetch warning:', err);
  }
}

// ── Fetch & Populate Dataset Stats ────────────────────────────────────────────
async function fetchDatasetStats() {
  try {
    const res = await fetch('/api/dataset/stats');
    if (!res.ok) return;

    const stats = await res.json();
    appState.datasetStats = stats;

    if (stats.target_distribution) {
      const t0 = stats.target_distribution.no_disease;
      const t1 = stats.target_distribution.disease_detected;
      const total = stats.total_records || (t0 + t1);
      const el0 = document.getElementById('target-count-0');
      const el1 = document.getElementById('target-count-1');
      if (el0) el0.textContent = `${t0} patients (${((t0 / total) * 100).toFixed(1)}%)`;
      if (el1) el1.textContent = `${t1} patients (${((t1 / total) * 100).toFixed(1)}%)`;
    }

    if (stats.sex_distribution) {
      const m = stats.sex_distribution.male;
      const f = stats.sex_distribution.female;
      const total = m + f;
      const elM = document.getElementById('sex-count-male');
      const elF = document.getElementById('sex-count-female');
      if (elM) elM.textContent = `${m} patients (${((m / total) * 100).toFixed(1)}%)`;
      if (elF) elF.textContent = `${f} patients (${((f / total) * 100).toFixed(1)}%)`;
    }
  } catch (err) {
    console.warn('Dataset stats fetch warning:', err);
  }
}

// ── Live Telemetry Heartbeat Simulation ───────────────────────────────────────
function initTelemetrySimulation() {
  if (!dom.liveBpmDisplay) return;

  let baseBpm = 72;
  setInterval(() => {
    // Subtle rhythmic variation +/- 2 BPM
    const delta = Math.floor(Math.random() * 5) - 2;
    const current = Math.max(68, Math.min(76, baseBpm + delta));
    dom.liveBpmDisplay.textContent = current;
  }, 2400);
}

// ── Scroll Spy for Navigation Links ───────────────────────────────────────────
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    let currentId = '';
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop - 120;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        currentId = section.getAttribute('id');
      }
    });

    dom.navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  });
}

// ── Toast Notification Helper ─────────────────────────────────────────────────
function showToast(message, type = 'info') {
  if (!dom.toastContainer) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type === 'error' ? 'error' : ''}`;
  
  const icon = type === 'error' ? '⚠️' : (type === 'success' ? '✓' : 'ℹ️');
  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;

  dom.toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 400);
  }, 4200);
}
