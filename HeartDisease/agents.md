# Heart Disease Detection ML Project - Agent Instructions

## Project Context

This is a BTech CSE project titled:

"Heart Disease Detection Using Machine Learning"

The project uses a machine learning model to predict whether heart disease is detected based on patient clinical attributes.

The project was previously developed on another computer and is now being continued on a different computer.

The existing project files are already present in this workspace.

IMPORTANT:
The existing frontend is NOT satisfactory and should NOT be treated as the final design.

We are restarting the frontend design and implementation from scratch.

---

## PRIMARY GOAL

Completely redesign and rebuild the frontend from scratch.

The new frontend should be:

- Modern
- Visually attractive
- Clean
- Professional
- Healthcare-focused
- Suitable for a BTech CSE project
- Responsive
- Easy to understand
- Easy to demonstrate during college presentation/viva

The frontend should look significantly better than the current implementation.

Do not simply modify the existing frontend styling.

Treat the current frontend as a prototype/reference only and rebuild the UI properly.

---

## VERY IMPORTANT: BEFORE CHANGING CODE

First inspect the entire existing project.

Understand:

1. Project structure
2. Frontend framework
3. Frontend entry points
4. Existing components
5. Existing routes
6. Existing backend/API
7. ML model integration
8. API request/response format
9. Existing dependencies
10. Existing environment variables
11. How the application currently runs

Do NOT immediately start rewriting files.

First determine what currently works and what must be preserved.

The project was created on another computer, so do not assume that the current environment has the same setup.

---

## FRONTEND REBUILD RULE

The frontend should be rebuilt from scratch.

Do NOT preserve the existing visual design just because it already exists.

However:

DO preserve working backend, ML, API, data-processing and prediction functionality unless there is a genuine technical reason to change it.

The goal is:

OLD FRONTEND
       ↓
REMOVE / REBUILD
       ↓
NEW FRONTEND
       ↓
CONNECT TO EXISTING ML/API

---

## DO NOT BREAK THE ML SYSTEM

The machine learning functionality is important.

The frontend must eventually communicate with the actual trained ML model through the existing backend/API.

DO NOT:

- Create fake ML predictions
- Hardcode prediction results
- Invent accuracy values
- Invent confidence values
- Replace the actual model with frontend logic
- Change model behavior just to make the UI work
- Create fake API responses

If the backend already exposes a prediction endpoint, use the existing endpoint.

If the API contract is unclear, inspect the backend before changing anything.

---

## ML INPUTS

The project is based on clinical patient attributes including:

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- Oldpeak
- Slope
- CA
- Thal

The frontend form should eventually correspond exactly to the actual features expected by the trained model/API.

Do NOT invent additional medical inputs.

Do NOT remove required model inputs without verifying the backend.

---

# DESIGN DIRECTION

The new UI should combine:

Healthcare
+
Machine Learning
+
Modern Web Design

The design should be visually impressive but still believable as a BTech student project.

Avoid making it look like:

- A generic hospital website
- A boring college project
- A generic SaaS dashboard
- A crypto website
- An overly futuristic AI interface
- An excessive glassmorphism template

---

## VISUAL STYLE

Preferred visual direction:

- Dark navy / midnight blue hero sections
- White/light content sections
- Cyan / electric blue accents
- Subtle gradients
- Soft blue glow
- Rounded cards
- Thin borders
- Soft shadows
- Modern typography
- Strong visual hierarchy
- Clean medical illustrations
- ECG / heartbeat visual elements
- Subtle animations
- Plenty of whitespace

Use visual elements intentionally.

Do not make every component glow.

Do not overuse gradients.

Do not overuse glassmorphism.

The UI should feel premium without becoming visually noisy.

---

# LANDING PAGE

Create a strong visual hero section.

Hero content:

Badge:
"Machine Learning • Healthcare"

Heading:

"Heart Disease Detection
Using Machine Learning"

Description:

"Analyze clinical patient attributes and generate a machine-learning-based prediction for heart disease."

Primary CTA:

"Start Prediction"

Secondary CTA:

"View Project"

Hero visual:

Create a large medical heart / ECG inspired visual.

The hero may use an animated background such as GradientWaves if it improves the design.

If GradientWaves is already installed or available in the project, use it appropriately.

Do not introduce unnecessary dependencies unless needed.

---

# WEBSITE STRUCTURE

The core website should contain:

## 1. Home

Sections:

- Hero
- Project introduction
- Key features
- How it works
- ML workflow
- CTA to prediction

---

## 2. Prediction

Create a dedicated prediction experience.

Heading:

"Heart Disease Prediction"

Subtitle:

"Enter the patient's clinical information to generate a prediction."

Create a visually polished form.

Fields:

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- Oldpeak
- Slope
- CA
- Thal

Use appropriate input types.

Categorical values should use dropdown/select controls where appropriate.

Numerical values should use number inputs.

The form should be easy to understand for a first-time user.

Primary button:

"Predict Heart Disease"

---

# RESULT EXPERIENCE

The prediction result should be visually prominent.

Possible actual model outputs:

"Heart Disease Detected"

or

"No Heart Disease Detected"

The result should clearly communicate the returned model prediction.

Use appropriate visual states.

Do NOT display fake:

- Accuracy
- Probability
- Confidence score
- Medical statistics

unless the backend actually provides those values.

Include:

"For educational purposes only. This system is not a medical diagnosis."

---

# ABOUT / PROJECT SECTION

Include:

## Problem Statement

Explain the project's purpose concisely.

## Proposed Solution

Explain the ML-based prediction system.

## Dataset

UCI Heart Disease Dataset.

## Workflow

Data Collection
→
Data Cleaning
→
EDA
→
Train/Test Split
→
Model Training
→
Evaluation
→
Prediction

## Algorithms

- Logistic Regression
- Decision Tree
- Random Forest
- K-Nearest Neighbors

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter / Google Colab

Do not invent model performance numbers.

---

# COMPONENT DESIGN

Create reusable components where appropriate.

Examples:

- Navbar
- Hero
- FeatureCard
- WorkflowStep
- PredictionForm
- FormField
- ResultCard
- AlgorithmCard
- TechnologyBadge
- Footer

Avoid creating unnecessary abstractions.

Keep the code understandable for a BTech student.

---

# RESPONSIVENESS

The website must work properly on:

- Desktop
- Laptop
- Tablet
- Mobile

Desktop:
- Spacious layouts
- Large hero
- Two-column prediction form where appropriate

Mobile:
- Single-column layout
- Hamburger navigation if necessary
- Full-width buttons
- Properly stacked cards
- Readable typography
- No horizontal overflow

---

# ANIMATIONS

Use subtle animations:

- Fade-in
- Slide-up
- Hover states
- Button transitions
- Card hover
- Smooth scrolling
- Background animation

Animations should improve the UI rather than distract from it.

Avoid excessive animation.

---

# CODE QUALITY

Keep the code:

- Clean
- Modular
- Readable
- Maintainable
- Consistent

Do not create unnecessary files.

Do not duplicate components.

Do not install libraries without a reason.

Use the existing project stack whenever possible.

Before installing a dependency, check whether an existing dependency can solve the requirement.

---

# API INTEGRATION

The frontend should communicate with the actual backend.

Before implementing the prediction form:

1. Inspect the backend.
2. Find the prediction endpoint.
3. Determine its HTTP method.
4. Determine the request body.
5. Determine the response format.
6. Determine how errors are returned.
7. Connect the frontend accordingly.

Do not guess the API contract.

If the existing API already works, do not rewrite it unnecessarily.

---

# ERROR HANDLING

The frontend should handle:

- Missing fields
- Invalid numerical values
- API errors
- Backend unavailable
- Prediction errors
- Loading state

Show clear user-friendly messages.

Do not expose raw stack traces to users.

---

# MEDICAL DISCLAIMER

This is an educational ML prototype.

The UI must clearly communicate:

"This system is for educational purposes only and is not a medical diagnosis."

Do not make medical claims that are not supported by the actual project.

---

# DEVELOPMENT PROCESS

Follow this order:

### Phase 1 — Inspect

Understand the existing project.

### Phase 2 — Plan

Create a short implementation plan for the frontend rebuild.

### Phase 3 — Clean Frontend

Identify which existing frontend files/components can be removed or replaced.

### Phase 4 — Build Design System

Establish:

- Colors
- Typography
- Spacing
- Buttons
- Cards
- Inputs
- Navigation
- Result states

### Phase 5 — Build Pages

Build:

Home
Prediction
Result
About

### Phase 6 — Responsive Design

Test desktop and mobile layouts.

### Phase 7 — Connect API

Connect the new prediction form to the existing backend/ML model.

### Phase 8 — Test

Verify:

- Frontend starts
- Backend starts
- API works
- Prediction works
- No console errors
- No broken routes
- No horizontal overflow
- Form validation works
- Loading states work
- Error states work

---

# IMPORTANT AGENT BEHAVIOR

Do not blindly rewrite the entire repository.

Do not delete backend or ML files.

Do not change the trained model unless explicitly asked.

Do not fabricate functionality.

Do not fabricate data.

Do not fabricate model results.

Do not stop after creating a visual mockup.

The final frontend must actually work with the existing project.

When uncertain about existing functionality, inspect the relevant code first.

Prioritize a polished, functional frontend over unnecessary features.

---

# SUCCESS CRITERIA

The project is successful when:

1. The new frontend looks substantially better than the previous frontend.
2. The UI is responsive.
3. The prediction form is complete.
4. The frontend connects to the real backend.
5. The backend uses the actual ML model.
6. Predictions displayed in the UI come from the real model.
7. No fake ML results are used.
8. The project can be demonstrated locally.
9. The code remains understandable for a BTech CSE student.
10. The website looks polished enough for a college project presentation.