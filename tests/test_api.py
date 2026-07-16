"""
tests/test_api.py - API Endpoint Tests
=======================================
Marketing Intelligence AI Platform

Integration tests for all API Blueprint endpoints.
"""

import pytest
from app import create_app
from config import TestingConfig


@pytest.fixture
def client():
    """Create a test Flask client with testing configuration."""
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Health check tests
# ---------------------------------------------------------------------------


def test_health_check_returns_200(client):
    """GET /health should return 200 with status ok."""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


# ---------------------------------------------------------------------------
# Upload API tests
# ---------------------------------------------------------------------------


def test_upload_no_file_returns_400(client):
    """POST /api/upload/ without a file should return 400."""
    response = client.post("/api/upload/")
    assert response.status_code == 400


def test_upload_list_returns_200(client):
    """GET /api/upload/list should return 200 and a files list."""
    response = client.get("/api/upload/list")
    assert response.status_code == 200
    data = response.get_json()
    assert "files" in data


# ---------------------------------------------------------------------------
# Revenue API tests
# ---------------------------------------------------------------------------


def test_revenue_predict_empty_body_returns_400(client):
    """POST /api/revenue/predict without JSON body should return 400."""
    response = client.post("/api/revenue/predict", content_type="application/json", data="")
    assert response.status_code == 400


def test_revenue_predict_returns_200_with_valid_body(client):
    """POST /api/revenue/predict with valid body should return 200."""
    # TODO: Replace with realistic test payload once model is integrated.
    response = client.post(
        "/api/revenue/predict",
        json={"data": [{"campaign_id": "c1", "spend": 100, "revenue": 500}]},
    )
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Anomaly API tests
# ---------------------------------------------------------------------------


def test_anomaly_detect_returns_200(client):
    """POST /api/anomaly/detect with valid body should return 200."""
    response = client.post(
        "/api/anomaly/detect",
        json={"data": [{"date": "2024-01-01", "clicks": 100, "impressions": 5000}]},
    )
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Segmentation API tests
# ---------------------------------------------------------------------------


def test_segmentation_segment_returns_200(client):
    """POST /api/segmentation/segment with valid body should return 200."""
    response = client.post(
        "/api/segmentation/segment",
        json={"data": [{"customer_id": "u1", "revenue": 200, "clicks": 50}]},
    )
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Creative API tests
# ---------------------------------------------------------------------------


def test_creative_score_returns_200(client):
    """POST /api/creative/score with valid body should return 200."""
    response = client.post(
        "/api/creative/score",
        json={"data": [{"creative_id": "cr1", "impressions": 10000, "clicks": 300}]},
    )
    assert response.status_code == 200
