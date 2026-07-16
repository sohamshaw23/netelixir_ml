# Marketing Intelligence AI Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

An AI-powered **Marketing Intelligence Platform** built with Flask that provides:

- 📉 **Revenue Drop Risk Prediction** — XGBoost + LightGBM ensemble with SHAP explanations
- 🔍 **Anomaly Detection** — Isolation Forest for identifying unusual campaign behaviour
- 👥 **Customer Segmentation** — K-Means clustering for audience intelligence
- 🎨 **Creative Performance Scoring** — CatBoost model to rank ad creatives

---

## Project Structure

```
marketing-intelligence-ai/
├── app.py                     # Flask application factory
├── run.py                     # Dev/production entry point
├── config.py                  # Environment-based configuration
├── settings.py                # Global runtime settings
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── api/                       # Flask Blueprints (REST API)
├── shared/                    # Shared utilities (logger, preprocess, etc.)
├── revenue_drop_risk/         # Revenue risk ML module
├── anomaly_detection/         # Anomaly detection ML module
├── customer_segmentation/     # Segmentation ML module
├── creative_performance/      # Creative scoring ML module
│
├── data/                      # Raw, processed, feature, and output data
├── models/                    # Serialised model artefacts
├── notebooks/                 # EDA and experiment notebooks
├── templates/                 # Jinja2 HTML templates
├── static/                    # CSS, JS, images
├── scripts/                   # Standalone training/evaluation scripts
├── tests/                     # Unit and integration tests
└── docs/                      # Architecture and API documentation
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-org/marketing-intelligence-ai.git
cd marketing-intelligence-ai
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your secrets and API keys
```

### 5. Run the development server

```bash
python run.py
# or
flask --app app run --debug
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Docker

```bash
docker-compose up --build
```

---

## API Endpoints

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|------------------------------------|
| GET    | `/health`                         | Health check                       |
| POST   | `/api/upload`                     | Upload a data CSV file             |
| POST   | `/api/revenue/predict`            | Revenue drop risk prediction       |
| POST   | `/api/anomaly/detect`             | Anomaly detection                  |
| POST   | `/api/segmentation/segment`       | Customer segmentation              |
| POST   | `/api/creative/score`             | Creative performance scoring       |

---

## Training Pipeline

```bash
# Train all models
python scripts/train_all.py

# Generate features
python scripts/generate_features.py

# Evaluate models
python scripts/evaluate.py
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Tech Stack

| Component          | Technology                    |
|--------------------|-------------------------------|
| Web Framework      | Flask 3.x + Blueprints        |
| ML Libraries       | XGBoost, LightGBM, CatBoost   |
| Explainability     | SHAP                          |
| Data Processing    | Pandas, NumPy, Scikit-learn   |
| Visualisation      | Plotly, Seaborn, Matplotlib   |
| Containerisation   | Docker + Docker Compose       |
| Production Server  | Gunicorn                      |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.
