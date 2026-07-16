"""
test_api.py

API Integration Tests

Run:
pytest tests/test_api.py
"""

import io
import json
import pytest


###############################################################
# Home Endpoint
###############################################################

def test_home(client):

    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert "project" in data or "Project" in data


###############################################################
# Health API
###############################################################

def test_health(client):

    response = client.get("/health/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"

    assert "available_models" in data


###############################################################
# Upload CSV
###############################################################

def test_upload_csv(client, upload_csv):

    response = client.post(

        "/upload/",

        data=upload_csv,

        content_type="multipart/form-data"

    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    assert "filepath" in data


###############################################################
# Invalid Upload
###############################################################

def test_invalid_upload(client, invalid_upload):

    response = client.post(

        "/upload/",

        data=invalid_upload,

        content_type="multipart/form-data"

    )

    assert response.status_code == 400


###############################################################
# Revenue API
###############################################################

def test_revenue_prediction(

    client,

    csv_file

):

    response = client.post(

        "/revenue/predict",

        json={

            "filepath": csv_file

        }

    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


###############################################################
# Anomaly API
###############################################################

def test_anomaly_prediction(

    client,

    csv_file

):

    response = client.post(

        "/anomaly/detect",

        json={

            "filepath": csv_file

        }

    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


###############################################################
# Segmentation API
###############################################################

def test_segmentation_prediction(

    client,

    csv_file

):

    response = client.post(

        "/segment/predict",

        json={

            "filepath": csv_file

        }

    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


###############################################################
# Creative API
###############################################################

def test_creative_prediction(

    client,

    csv_file

):

    response = client.post(

        "/creative/predict",

        json={

            "filepath": csv_file

        }

    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


###############################################################
# Missing filepath
###############################################################

@pytest.mark.parametrize(

    "endpoint",

    [

        "/revenue/predict",

        "/anomaly/detect",

        "/segment/predict",

        "/creative/predict"

    ]

)

def test_missing_filepath(

    client,

    endpoint

):

    response = client.post(

        endpoint,

        json={}

    )

    assert response.status_code == 400


###############################################################
# Invalid filepath
###############################################################

@pytest.mark.parametrize(

    "endpoint",

    [

        "/revenue/predict",

        "/anomaly/detect",

        "/segment/predict",

        "/creative/predict"

    ]

)

def test_invalid_filepath(

    client,

    endpoint

):

    response = client.post(

        endpoint,

        json={

            "filepath":

            "abc.csv"

        }

    )

    assert response.status_code in [

        404,

        500

    ]


###############################################################
# Wrong Request Type
###############################################################

def test_wrong_method(client):

    response = client.get(

        "/revenue/predict"

    )

    assert response.status_code == 405


###############################################################
# Empty JSON
###############################################################

def test_empty_json(

    client

):

    response = client.post(

        "/revenue/predict",

        data="",

        content_type="application/json"

    )

    assert response.status_code in [

        400,

        415

    ]


###############################################################
# Invalid Route
###############################################################

def test_invalid_route(client):

    response = client.get(

        "/abcd"

    )

    assert response.status_code == 404


###############################################################
# Upload without file
###############################################################

def test_upload_without_file(

    client

):

    response = client.post(

        "/upload/",

        data={},

        content_type="multipart/form-data"

    )

    assert response.status_code == 400


###############################################################
# Upload Empty Filename
###############################################################

def test_empty_filename(

    client

):

    data = {

        "file": (

            io.BytesIO(

                b""

            ),

            ""

        )

    }

    response = client.post(

        "/upload/",

        data=data,

        content_type="multipart/form-data"

    )

    assert response.status_code == 400

