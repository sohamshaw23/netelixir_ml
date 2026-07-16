"""
api/upload.py - File Upload Blueprint
======================================
Marketing Intelligence AI Platform

Handles CSV / Excel file uploads from the browser or API clients and saves
them to the configured uploads directory for downstream processing.
"""

import logging
import os
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

upload_blueprint = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _allowed_file(filename: str) -> bool:
    """Return True if *filename* has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@upload_blueprint.route("/", methods=["POST"])
def upload_file():
    """
    Upload a data file (CSV or Excel).

    Request:
        multipart/form-data with field ``file``.

    Returns:
        JSON: { "message": str, "filename": str, "path": str }

    TODO:
        - Validate schema of uploaded CSV (required columns, dtypes).
        - Trigger asynchronous pre-processing pipeline.
        - Store file metadata in the database.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not _allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed. Allowed: {ALLOWED_EXTENSIONS}"}), 415

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    save_path = Path(upload_folder) / filename
    file.save(save_path)

    logger.info("File uploaded successfully: %s", save_path)

    # TODO: Kick off data validation and pre-processing pipeline here.

    return jsonify({
        "message": "File uploaded successfully.",
        "filename": filename,
        "path": str(save_path),
    }), 201


@upload_blueprint.route("/list", methods=["GET"])
def list_uploads():
    """
    List all uploaded files.

    Returns:
        JSON: { "files": [str, ...] }

    TODO: Return file metadata (size, upload time, status) from the database.
    """
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    files = [f for f in os.listdir(upload_folder) if _allowed_file(f)]
    return jsonify({"files": files}), 200
