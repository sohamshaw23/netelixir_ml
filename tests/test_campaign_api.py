"""
tests/test_campaign_api.py

Integration tests for the Campaign Intelligence APIs.
"""

import json
import pytest


def test_predict_revenue(client):
    """
    Test static revenue prediction endpoint.
    """
    payload = {
        "date": "2026-07-17",
        "platform": "google",
        "spend": 100.0,
        "clicks": 200,
        "impressions": 5000,
        "conversions": 10,
        "campaign_name": "Google_Search_Brand"
    }
    response = client.post(
        "/campaign/predict_revenue",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "predicted_revenue" in data
    assert isinstance(data["predicted_revenue"], float)
    assert "model_metrics" in data
    assert data["model_metrics"]["r2"] == 0.9161


def test_predict_roas(client):
    """
    Test static ROAS prediction endpoint.
    """
    payload = {
        "date": "2026-07-17",
        "platform": "google",
        "spend": 100.0,
        "clicks": 200,
        "impressions": 5000,
        "conversions": 10,
        "campaign_name": "Google_Search_Brand"
    }
    response = client.post(
        "/campaign/predict_roas",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "predicted_roas" in data
    assert isinstance(data["predicted_roas"], float)
    assert "model_metrics" in data
    assert data["model_metrics"]["r2"] == 0.7157


def test_predict_campaign(client):
    """
    Test time-series campaign revenue prediction endpoint.
    """
    payload = {
        "date": "2026-07-17",
        "platform": "google",
        "spend": 100.0,
        "clicks": 200,
        "impressions": 5000,
        "conversions": 10,
        "campaign_name": "Google_Search_Brand"
    }
    response = client.post(
        "/campaign/predict_campaign",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "predicted_campaign_revenue" in data
    assert isinstance(data["predicted_campaign_revenue"], float)
    assert "recommendation" in data
    assert data["recommendation"] in ["Increase Budget", "Maintain Budget"]
    assert "model_metrics" in data
    assert data["model_metrics"]["r2"] == 0.82


def test_predict_channel(client):
    """
    Test time-series channel revenue prediction endpoint.
    """
    payload = {
        "date": "2026-07-17",
        "platform": "google",
        "spend": 100.0,
        "clicks": 200,
        "impressions": 5000,
        "conversions": 10
    }
    response = client.post(
        "/campaign/predict_channel",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "predicted_channel_revenue" in data
    assert isinstance(data["predicted_channel_revenue"], float)
    assert "model_metrics" in data
    assert data["model_metrics"]["r2"] == 0.9060


def test_empty_json(client):
    """
    Test API bad request handling on empty payload.
    """
    response = client.post(
        "/campaign/predict_revenue",
        data="",
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "message" in data
