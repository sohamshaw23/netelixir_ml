"""
upload.py
---------

File Upload API

Supported Files:
- CSV
- XLSX

Endpoint:
POST /upload
"""

import os
import uuid
from pathlib import Path

from flask import Blueprint
from flask import jsonify
from flask import request

from werkzeug.utils import secure_filename


upload_bp = Blueprint(
    "upload",
    __name__
)

###########################################################

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_FOLDER = BASE_DIR / "uploads"

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

###########################################################

ALLOWED_EXTENSIONS = {

    "csv",

    "xlsx"

}

###########################################################


def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(".", 1)[1].lower()

        in ALLOWED_EXTENSIONS

    )


###########################################################


@upload_bp.route(

    "/",

    methods=["POST"]

)

def upload_file():

    try:

        if "file" not in request.files:

            return jsonify({

                "success": False,

                "message": "No file uploaded."

            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({

                "success": False,

                "message": "Empty filename."

            }), 400

        if not allowed_file(file.filename):

            return jsonify({

                "success": False,

                "message":
                "Only CSV and XLSX files are supported."

            }), 400

        extension = file.filename.rsplit(".", 1)[1].lower()

        filename = (

            str(uuid.uuid4())

            + "."

            + extension

        )

        filename = secure_filename(filename)

        filepath = UPLOAD_FOLDER / filename

        file.save(filepath)

        return jsonify({

            "success": True,

            "filename": filename,

            "filepath": str(filepath),

            "message": "File uploaded successfully."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500

