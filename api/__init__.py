"""
API Package
===========

Contains all Flask Blueprints.

Endpoints

/health
/upload
/revenue
/anomaly
/segment
/creative
"""

from flask import Blueprint

api = Blueprint(

    "api",

    __name__

)

