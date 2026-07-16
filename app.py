"""
app.py

Marketing Intelligence Platform

Main Flask Application

Author : Team AIgnition
Version : 1.0.0
"""

from flask import Flask
from flask import jsonify

from flask_cors import CORS

from config import config

from api.routes import register_routes

from shared.logger import get_logger

from models import registry


############################################################
# Create Flask App
############################################################

app = Flask(__name__)

############################################################
# Load Configuration
############################################################

app.config.from_object(

    config["development"]

)

############################################################
# Enable CORS
############################################################

CORS(

    app,

    resources={

        r"/*": {

            "origins": "*"

        }

    }

)

############################################################
# Logger
############################################################

logger = get_logger(

    "MarketingAI"

)

############################################################
# Register Routes
############################################################

register_routes(app)

############################################################
# Load Models
############################################################

try:

    registry.load_all()

    logger.info(

        "All ML Models Loaded Successfully."

    )

except Exception as e:

    logger.exception(

        "Model Loading Failed"

    )

############################################################
# Root Route
############################################################

@app.route(

    "/",

    methods=["GET"]

)

def home():

    return jsonify(

        {

            "project":

                "Marketing Intelligence Platform",

            "version":

                "1.0.0",

            "status":

                "Running",

            "models":[

                "Revenue Drop Risk",

                "Anomaly Detection",

                "Customer Segmentation",

                "Creative Performance"

            ],

            "api":[

                "/health",

                "/upload",

                "/revenue/predict",

                "/anomaly/detect",

                "/segment/predict",

                "/creative/predict"

            ]

        }

    )

############################################################
# Error Handlers
############################################################

@app.errorhandler(404)

def page_not_found(error):

    return jsonify(

        {

            "success": False,

            "message": "Endpoint Not Found"

        }

    ),404


############################################################

@app.errorhandler(405)

def method_not_allowed(error):

    return jsonify(

        {

            "success": False,

            "message": "Method Not Allowed"

        }

    ),405


############################################################

@app.errorhandler(413)

def file_too_large(error):

    return jsonify(

        {

            "success": False,

            "message":

            "Uploaded file is too large."

        }

    ),413


############################################################

@app.errorhandler(500)

def internal_server_error(error):

    logger.exception(error)

    return jsonify(

        {

            "success": False,

            "message":

            "Internal Server Error"

        }

    ),500


############################################################
# Before Request
############################################################

@app.before_request

def before_request():

    logger.info(

        "Incoming Request"

    )

############################################################
# After Request
############################################################

@app.after_request

def after_request(response):

    response.headers[

        "X-Powered-By"

    ] = "Marketing Intelligence Platform"

    return response

############################################################
# Health Check
############################################################

@app.route(

    "/ping"

)

def ping():

    return {

        "status":"OK"

    }

############################################################

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )

