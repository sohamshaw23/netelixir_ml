# Deployment Guide

## Marketing Intelligence AI Platform

---

## Local Development

```bash
# 1. Clone and enter the project
git clone https://github.com/your-org/marketing-intelligence-ai.git
cd marketing-intelligence-ai

# 2. Create virtual environment
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env  # or edit .env directly

# 5. Start the development server
python run.py
# App runs at http://localhost:5000
```

---

## Docker (Recommended for Production)

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

---

## Production with Gunicorn

```bash
# Install production dependencies
pip install gunicorn

# Start with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 "app:app"
```

---

## Environment Variables

| Variable           | Required | Description                          |
|--------------------|----------|--------------------------------------|
| `SECRET_KEY`       | ✅        | Flask session secret key             |
| `FLASK_ENV`        | ✅        | `development` or `production`        |
| `PORT`             | ❌        | Port to bind (default: 5000)         |
| `DATABASE_URL`     | ❌        | Database connection string           |
| `LOG_LEVEL`        | ❌        | Logging level (default: INFO)        |
| `MODEL_VERSION`    | ❌        | Active model version (default: v1.0) |

---

## Training Models

```bash
# Clean raw data
python scripts/clean_data.py

# Generate features
python scripts/generate_features.py

# Train all models
python scripts/train_all.py

# Evaluate
python scripts/evaluate.py
```

---

## Running Tests

```bash
pytest tests/ -v --tb=short
```

---

## Monitoring

- **Health check:** `GET /health/` — returns uptime and service status.
- **Readiness:** `GET /health/ready` — returns 503 if models/data not ready.
- TODO: Integrate Prometheus metrics endpoint.
- TODO: Configure Grafana dashboard for API latency and error rates.

---

## CI/CD (TODO)

- Configure GitHub Actions workflow in `.github/workflows/`.
- Steps: lint → test → build Docker image → push to registry → deploy.
