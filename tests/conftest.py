"""
conftest.py

Shared pytest fixtures for the project.
"""

import io
import tempfile

import pandas as pd
import pytest

from app import app


##############################################################
# Flask Test Client
##############################################################

@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.test_client() as client:

        yield client


##############################################################
# Sample Marketing Dataset
##############################################################

@pytest.fixture
def sample_dataframe():

    data = {

        "Spend": [1000, 2000, 3500, 5000],

        "Revenue": [4500, 7000, 9200, 12000],

        "Clicks": [120, 250, 380, 510],

        "Impressions": [8000, 12000, 15000, 25000],

        "CTR": [0.015, 0.021, 0.025, 0.020],

        "CPC": [8.33, 8.00, 9.21, 9.80],

        "Conversions": [12, 28, 41, 60],

        "ROAS": [4.5, 3.5, 2.6, 2.4],

        "CampaignType": [

            "Search",

            "Display",

            "Video",

            "Social"

        ],

        "Device": [

            "Mobile",

            "Desktop",

            "Tablet",

            "Mobile"

        ],

        "Channel": [

            "Google",

            "Meta",

            "YouTube",

            "Instagram"

        ],

        "Audience": [

            "Students",

            "Professionals",

            "Parents",

            "Gamers"

        ],

        "CreativeType": [

            "Image",

            "Video",

            "Carousel",

            "Banner"

        ]

    }

    return pd.DataFrame(data)


##############################################################
# Temporary CSV File
##############################################################

@pytest.fixture
def csv_file(sample_dataframe):

    temp = tempfile.NamedTemporaryFile(

        suffix=".csv",

        delete=False

    )

    sample_dataframe.to_csv(

        temp.name,

        index=False

    )

    temp.close()

    return temp.name


##############################################################
# Temporary Excel File
##############################################################

@pytest.fixture
def excel_file(sample_dataframe):

    temp = tempfile.NamedTemporaryFile(

        suffix=".xlsx",

        delete=False

    )

    sample_dataframe.to_excel(

        temp.name,

        index=False

    )

    temp.close()

    return temp.name


##############################################################
# Upload File Fixture
##############################################################

@pytest.fixture
def upload_csv():

    csv_content = (
        "Spend,Revenue,Clicks\n"
        "1000,5000,120\n"
        "2000,7000,250\n"
    )

    return {

        "file": (

            io.BytesIO(

                csv_content.encode()

            ),

            "marketing.csv"

        )

    }


##############################################################
# Invalid Upload
##############################################################

@pytest.fixture
def invalid_upload():

    return {

        "file": (

            io.BytesIO(

                b"Hello"

            ),

            "file.txt"

        )

    }
