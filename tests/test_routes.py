"""
test_routes.py

Tests Flask routing and blueprint registration.

Run:
pytest tests/test_routes.py
"""

from api.routes import register_routes
from flask import Flask


###############################################################
# App Fixture
###############################################################

def create_test_app():

    app = Flask(__name__)

    register_routes(app)

    return app


###############################################################
# Blueprint Registration
###############################################################

def test_blueprints_registered():

    app = create_test_app()

    expected = {

        "health",

        "upload",

        "revenue",

        "anomaly",

        "segmentation",

        "creative"

    }

    registered = set(app.blueprints.keys())

    assert expected.issubset(registered)


###############################################################
# URL Rules
###############################################################

def test_registered_routes():

    app = create_test_app()

    routes = {

        rule.rule

        for rule in app.url_map.iter_rules()

    }

    assert "/health/" in routes

    assert "/upload/" in routes

    assert "/revenue/predict" in routes

    assert "/anomaly/detect" in routes

    assert "/segment/predict" in routes

    assert "/creative/predict" in routes


###############################################################
# Endpoint Names
###############################################################

def test_endpoint_names():

    app = create_test_app()

    endpoints = {

        rule.endpoint

        for rule in app.url_map.iter_rules()

    }

    assert "health.health" in endpoints

    assert "upload.upload_file" in endpoints

    assert "revenue.predict" in endpoints

    assert "anomaly.detect" in endpoints

    assert "segmentation.predict" in endpoints

    assert "creative.predict" in endpoints


###############################################################
# Duplicate Route Check
###############################################################

def test_no_duplicate_routes():

    app = create_test_app()

    rules = [

        rule.rule

        for rule in app.url_map.iter_rules()

    ]

    assert len(rules) == len(set(rules))


###############################################################
# Allowed HTTP Methods
###############################################################

def test_http_methods():

    app = create_test_app()

    methods = {}

    for rule in app.url_map.iter_rules():

        methods[rule.rule] = rule.methods

    assert "GET" in methods["/health/"]

    assert "POST" in methods["/upload/"]

    assert "POST" in methods["/revenue/predict"]

    assert "POST" in methods["/anomaly/detect"]

    assert "POST" in methods["/segment/predict"]

    assert "POST" in methods["/creative/predict"]


###############################################################
# Unknown Route
###############################################################

def test_unknown_route(client):

    response = client.get(

        "/this_route_does_not_exist"

    )

    assert response.status_code == 404


###############################################################
# Wrong Method
###############################################################

def test_wrong_method(client):

    response = client.get(

        "/creative/predict"

    )

    assert response.status_code == 405


###############################################################
# OPTIONS Requests
###############################################################

def test_options_requests(client):

    response = client.options(

        "/revenue/predict"

    )

    assert response.status_code in [

        200,

        204

    ]


###############################################################
# URL Map Exists
###############################################################

def test_url_map():

    app = create_test_app()

    assert len(

        list(app.url_map.iter_rules())

    ) > 0

