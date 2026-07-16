"""
revenue_api.py

Revenue Drop Risk Prediction API

Endpoint

POST /revenue/predict
"""

from werkzeug.exceptions import HTTPException
from pathlib import Path

import pandas as pd

from flask import Blueprint
from flask import jsonify
from flask import request

from revenue_drop_risk.inference import (
    predict_revenue_risk
)


revenue_bp = Blueprint(

    "revenue",

    __name__

)

###########################################################


def load_dataframe(filepath):

    extension = Path(filepath).suffix.lower()

    if extension == ".csv":

        return pd.read_csv(filepath)

    elif extension in [".xlsx", ".xls"]:

        return pd.read_excel(filepath)

    else:

        raise ValueError(

            "Unsupported file format."

        )


###########################################################


@revenue_bp.route(

    "/predict",

    methods=["POST"]

)

def predict():

    try:

        body = request.get_json()

        if body is None:

            return jsonify({

                "success": False,

                "message": "JSON body required."

            }), 400

        filepath = body.get("filepath")

        if not filepath:

            return jsonify({

                "success": False,

                "message": "filepath missing."

            }), 400

        dataframe = load_dataframe(filepath)

        prediction = predict_revenue_risk(

            dataframe

        )

        return jsonify({

            "success": True,

            "prediction": prediction

        })

    except FileNotFoundError:

        return jsonify({

            "success": False,

            "message": "Dataset not found."

        }), 404

    except HTTPException as error:

        return jsonify({

            "success": False,

            "message": error.description

        }), error.code

    except Exception as error:

        return jsonify({

            "success": False,

            "message": str(error)

        }), 500

