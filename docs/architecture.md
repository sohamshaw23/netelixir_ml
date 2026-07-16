# Architecture Overview

## Marketing Intelligence AI Platform

### High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                        Client (Browser)                            │
└──────────────────────────┬─────────────────────────────────────────┘
                           │ HTTP / REST
┌──────────────────────────▼─────────────────────────────────────────┐
│                   Flask Application (app.py)                       │
│  ┌──────────┐  ┌───────────┐  ┌───────────┐  ┌──────────────────┐ │
│  │ routes   │  │  upload   │  │  health   │  │  (future: auth)  │ │
│  │Blueprint │  │ Blueprint │  │ Blueprint │  │                  │ │
│  └──────────┘  └───────────┘  └───────────┘  └──────────────────┘ │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────┐│
│  │ revenue_api  │  │ anomaly_api  │  │ segment_api  │  │creative││
│  │  Blueprint   │  │  Blueprint   │  │  Blueprint   │  │  API   ││
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └───┬────┘│
└─────────┼─────────────────┼─────────────────┼──────────────┼─────┘
          │                 │                 │              │
┌─────────▼─────────────────▼─────────────────▼──────────────▼─────┐
│                         ML Modules                                 │
│  ┌──────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ revenue_drop_risk│  │anomaly_detection│  │customer_segment │  │
│  │  XGBoost+LightGBM│  │ IsolationForest │  │   K-Means       │  │
│  │  + SHAP          │  │                 │  │                 │  │
│  └──────────────────┘  └─────────────────┘  └─────────────────┘  │
│  ┌──────────────────┐                                              │
│  │creative_perform  │                                              │
│  │  CatBoost        │                                              │
│  └──────────────────┘                                              │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    shared/ utilities                         │  │
│  │  data_loader │ preprocess │ feature_engineering │ metrics   │  │
│  │  visualization │ logger │ constants │ helper │ validation   │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
          │
┌─────────▼─────────────────────────────────────────────────────────┐
│                        Data Layer                                  │
│  data/raw/  │  data/processed/  │  data/features/  │ data/outputs │
│  models/                        │  uploads/                       │
└───────────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Blueprint Architecture** — Each feature domain (revenue, anomaly, segmentation, creative) is isolated in its own Flask Blueprint for maintainability.

2. **Module Isolation** — Each ML module is a standalone Python package with its own `config.py`, `model.py`, `preprocess.py`, `train.py`, and `inference.py`.

3. **Shared Utilities** — Common logic (logging, data loading, preprocessing, metrics) lives in `shared/` to avoid duplication.

4. **Application Factory Pattern** — `create_app()` in `app.py` enables easy testing with different configurations.

5. **Configuration Classes** — `DevelopmentConfig`, `TestingConfig`, `ProductionConfig` in `config.py` allow environment-specific settings without code changes.

### Data Flow

```
Raw CSV files → DataLoader → FeatureEngineer → SharedPreprocessor
→ ML Module (train/inference) → Predictions → API Response / CSV Output
```

### Future Enhancements

- Add PostgreSQL / Redis for persistent storage and caching.
- Add Celery for asynchronous model inference tasks.
- Add MLflow for experiment tracking and model registry.
- Add authentication (JWT / OAuth2).
- Add CI/CD pipeline (GitHub Actions).
