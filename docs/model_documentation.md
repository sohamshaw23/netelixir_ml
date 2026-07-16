# Model Documentation

## Marketing Intelligence AI Platform

---

## 1. Revenue Drop Risk Model

### Problem Statement
Predict whether a campaign will experience a significant revenue drop (>X%) in the next N days.

### Model Type
Binary Classification — XGBoost + LightGBM Soft-Voting Ensemble

### Inputs (Features)
- Campaign spend, clicks, impressions, conversions
- Derived: CTR, CPC, ROAS
- Rolling averages (7-day, 14-day, 30-day)
- Channel, day-of-week, week-of-year

### Target
`revenue_drop_flag` — 1 if revenue drops by > threshold%, else 0

### Explainability
SHAP TreeExplainer provides per-prediction feature importance values.

### Output
`risk_score` (0.0–1.0) and `risk_label` (Low / Medium / High Risk)

### TODO
- [ ] Define revenue drop threshold from business requirements
- [ ] Train and validate on historical data
- [ ] Calibrate risk thresholds on validation set

---

## 2. Anomaly Detection Model

### Problem Statement
Identify unusual patterns in campaign metrics that deviate from expected behaviour.

### Model Type
Unsupervised — Isolation Forest

### Inputs (Features)
- Daily campaign metrics: spend, clicks, impressions, conversions, ROAS, CTR

### Output
`anomaly_score` (decision function value) and `is_anomaly` (boolean)

### TODO
- [ ] Determine contamination rate from historical anomaly labels
- [ ] Calibrate anomaly score threshold
- [ ] Validate against known anomaly events

---

## 3. Customer Segmentation Model

### Problem Statement
Group customers into meaningful behavioural segments for targeted marketing.

### Model Type
Unsupervised — K-Means Clustering

### Inputs (Features)
- RFM features: Recency, Frequency, Monetary value
- Channel-level engagement metrics

### Output
`segment` (cluster ID) and `segment_label` (business name)

### TODO
- [ ] Run Elbow method and Silhouette analysis to determine optimal K
- [ ] Assign business-meaningful labels to each cluster
- [ ] Validate segment stability across time windows

---

## 4. Creative Performance Model

### Problem Statement
Predict and rank ad creatives by expected performance to guide creative investment.

### Model Type
Regression — CatBoost

### Inputs (Features)
- Creative attributes: format, copy length, call-to-action type
- Historical performance: CTR, ROAS, conversion rate
- Audience targeting parameters

### Target
`creative_performance_score` — composite metric (TBD after EDA)

### Output
`score` (continuous) and `rank` (integer)

### TODO
- [ ] Define performance score formula with stakeholders
- [ ] Collect sufficient training data (minimum impressions threshold)
- [ ] Validate model on held-out creative set

---

## Model Versioning

All models are versioned using the `MODEL_VERSION` environment variable (default: `v1.0`).
Future releases should use semantic versioning (`v1.1`, `v2.0`, etc.) and track
experiments in MLflow or Weights & Biases.
