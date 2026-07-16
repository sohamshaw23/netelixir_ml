"""
tests/test_routes.py - Route Integration Tests
===============================================
Marketing Intelligence AI Platform

Tests that all HTML page routes return the correct status codes and templates.
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


def test_index_returns_200(client):
    """GET / should render the index page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Marketing" in response.data


def test_dashboard_returns_200(client):
    """GET /dashboard should render the dashboard page."""
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_upload_page_returns_200(client):
    """GET /upload should render the upload page."""
    response = client.get("/upload")
    assert response.status_code == 200


def test_result_page_returns_200(client):
    """GET /result should render the result page."""
    response = client.get("/result")
    assert response.status_code == 200


def test_health_returns_200(client):
    """GET /health/ should return health status JSON."""
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.is_json
