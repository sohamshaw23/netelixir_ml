"""
scripts/__init__.py - Scripts Package
=======================================
Marketing Intelligence AI Platform

Makes the scripts/ directory an importable Python package so individual
pipeline functions can be called programmatically from other modules or
from a test suite without subprocess overhead.

Available Scripts
-----------------
train_all.py        — Train all ML models sequentially.
predict_all.py      — Run batch inference for all modules.
clean_data.py       — Merge and clean raw data sources.
generate_features.py — Run the full feature engineering pipeline.
evaluate.py         — Evaluate all models on the test set.

Quick Start
-----------
Run any script from the project root:

    python scripts/train_all.py
    python scripts/predict_all.py --help
    python scripts/clean_data.py
    python scripts/generate_features.py
    python scripts/evaluate.py

Or import and call a function directly:

    from scripts.train_all import train_revenue_model
    train_revenue_model()
"""
