# API Documentation

## Marketing Intelligence AI Platform

Base URL: `http://localhost:5000`

---

## Authentication

> TODO: Authentication is not yet implemented. JWT-based auth will be added in a future release.

---

## Health Endpoints

### `GET /health/`

**Description:** Liveness probe.

**Response:**
```json
{
  "status": "ok",
  "uptime_seconds": 123.45,
  "python_version": "3.11.x",
  "platform": "...",
  "service": "Marketing Intelligence AI Platform"
}
```

### `GET /health/ready`

**Description:** Readiness probe. Returns 503 if models or data are not ready.

---

## Upload Endpoints

### `POST /api/upload/`

**Description:** Upload a CSV or Excel file.

**Request:** `multipart/form-data` with field `file`.

**Response (201):**
```json
{
  "message": "File uploaded successfully.",
  "filename": "google_ads.csv",
  "path": "uploads/google_ads.csv"
}
```

### `GET /api/upload/list`

**Description:** List all uploaded files.

**Response (200):**
```json
{ "files": ["google_ads.csv", "meta_ads.csv"] }
```

---

## Revenue Drop Risk Endpoints

### `POST /api/revenue/predict`

**Description:** Predict revenue drop risk for campaign records.

**Request Body:**
```json
{
  "data": [
    { "campaign_id": "c1", "spend": 1000, "revenue": 5000, "clicks": 200 }
  ]
}
```

**Response (200):**
```json
{
  "predictions": [
    { "campaign_id": "c1", "risk_score": 0.82, "risk_label": "High Risk" }
  ]
}
```

### `POST /api/revenue/explain`

**Description:** Return SHAP explanation for a single revenue prediction.

### `GET /api/revenue/history`

**Description:** Return historical predictions.

---

## Anomaly Detection Endpoints

### `POST /api/anomaly/detect`

**Description:** Detect anomalies in campaign metric records.

**Request Body:**
```json
{
  "data": [
    { "date": "2024-01-15", "clicks": 10, "impressions": 500 }
  ]
}
```

**Response (200):**
```json
{
  "anomalies": [
    { "index": 0, "score": -0.45, "is_anomaly": true, "label": "anomaly" }
  ]
}
```

### `GET /api/anomaly/summary`

**Description:** Return anomaly summary over a date range.

---

## Customer Segmentation Endpoints

### `POST /api/segmentation/segment`

**Description:** Assign customers to segments.

**Request Body:**
```json
{ "data": [{ "customer_id": "u1", "revenue": 200, "clicks": 50 }] }
```

**Response (200):**
```json
{
  "segments": [
    { "customer_id": "u1", "segment": 2, "segment_label": "High Value" }
  ]
}
```

### `GET /api/segmentation/profiles`

**Description:** Return cluster profiles.

### `GET /api/segmentation/visualise`

**Description:** Return Plotly-compatible 2-D projection data.

---

## Creative Performance Endpoints

### `POST /api/creative/score`

**Description:** Score and rank ad creatives.

**Request Body:**
```json
{ "data": [{ "creative_id": "cr1", "impressions": 10000, "clicks": 300 }] }
```

**Response (200):**
```json
{
  "scores": [
    { "creative_id": "cr1", "score": 0.91, "rank": 1 }
  ]
}
```

### `POST /api/creative/importance`

**Description:** Return feature importances driving creative predictions.

### `GET /api/creative/top`

**Description:** Return top-performing creatives from the last scoring run.
