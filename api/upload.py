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


@upload_bp.route("/audit", methods=["POST"])
def audit_file():
    import pandas as pd
    try:
        body = request.get_json()
        if not body or "filepath" not in body:
            return jsonify({"success": False, "message": "filepath missing."}), 400
        
        filepath = Path(body["filepath"])
        if not filepath.exists():
            return jsonify({"success": False, "message": "File not found."}), 404
        
        # Load file
        extension = filepath.suffix.lower()
        if extension == ".csv":
            df = pd.read_csv(filepath)
        elif extension in [".xlsx", ".xls"]:
            df = pd.read_excel(filepath)
        else:
            return jsonify({"success": False, "message": "Unsupported file format."}), 400
        
        # Determine standard column mapping
        col_mapping = {}
        for col in df.columns:
            lcol = col.lower().strip()
            if "spend" in lcol:
                col_mapping["spend"] = col
            elif "click" in lcol:
                col_mapping["clicks"] = col
            elif "impression" in lcol:
                col_mapping["impressions"] = col
            elif "conversion" in lcol:
                col_mapping["conversions"] = col
            elif "revenue" in lcol:
                col_mapping["revenue"] = col
            elif "channel" in lcol or "platform" in lcol:
                col_mapping["channel"] = col
            elif "campaign" in lcol:
                col_mapping["campaign_name"] = col
            elif "date" in lcol:
                col_mapping["date"] = col
        
        errors = []
        # Check standard columns existence
        req_cols = ["date", "spend", "clicks", "impressions", "conversions", "revenue"]
        for rc in req_cols:
            if rc not in col_mapping:
                errors.append({
                    "row": 0,
                    "field": rc,
                    "issue": f"Required column '{rc}' is missing from the dataset.",
                    "severity": "danger"
                })
        
        # Perform row level validation if required columns exist
        if not any(e["severity"] == "danger" for e in errors):
            spend_col = col_mapping["spend"]
            clicks_col = col_mapping["clicks"]
            impr_col = col_mapping["impressions"]
            conv_col = col_mapping["conversions"]
            rev_col = col_mapping["revenue"]
            
            # Row loop
            for idx, row in df.iterrows():
                row_num = idx + 1
                
                # Check null values
                if row.isnull().any():
                    null_fields = list(row[row.isnull()].index)
                    errors.append({
                        "row": row_num,
                        "field": null_fields[0],
                        "issue": "Null/missing cell value detected.",
                        "severity": "warning"
                    })
                    if len(errors) >= 50:
                        break
                
                # Clicks vs Impressions check
                if row[clicks_col] > row[impr_col]:
                    errors.append({
                        "row": row_num,
                        "field": "clicks",
                        "issue": f"Clicks ({int(row[clicks_col])}) cannot exceed impressions ({int(row[impr_col])}).",
                        "severity": "warning"
                    })
                    if len(errors) >= 50:
                        break
                        
                # Conversions vs Clicks check
                if row[conv_col] > row[clicks_col]:
                    errors.append({
                        "row": row_num,
                        "field": "conversions",
                        "issue": f"Conversions ({int(row[conv_col])}) cannot exceed clicks ({int(row[clicks_col])}).",
                        "severity": "warning"
                    })
                    if len(errors) >= 50:
                        break
                        
                # Negative spend check
                if row[spend_col] < 0:
                    errors.append({
                        "row": row_num,
                        "field": "spend",
                        "issue": "Negative spend value detected.",
                        "severity": "danger"
                    })
                    if len(errors) >= 50:
                        break
                        
                # Negative revenue check
                if row[rev_col] < 0:
                    errors.append({
                        "row": row_num,
                        "field": "revenue",
                        "issue": "Negative revenue value detected.",
                        "severity": "danger"
                    })
                    if len(errors) >= 50:
                        break
        
        # Summary counts
        chan_field = col_mapping.get("channel", None)
        camp_field = col_mapping.get("campaign_name", None)
        spend_field = col_mapping.get("spend", None)
        
        channel_count = df[chan_field].nunique() if chan_field and chan_field in df.columns else 1
        campaign_count = df[camp_field].nunique() if camp_field and camp_field in df.columns else 1
        total_spend = float(df[spend_field].sum()) if spend_field and spend_field in df.columns else 0.0
        
        # Format preview rows
        preview_rows = []
        for idx, row in df.head(5).iterrows():
            preview_rows.append({
                "date": str(row.get(col_mapping.get("date", "Date"), "2026-07-01")),
                "campaignName": str(row.get(col_mapping.get("campaign_name", "campaign_name"), "N/A")),
                "channel": str(row.get(col_mapping.get("channel", "channel"), "N/A")),
                "spend": float(row.get(col_mapping.get("spend", "spend"), 0.0)),
                "clicks": int(row.get(col_mapping.get("clicks", "clicks"), 0)),
                "revenue": float(row.get(col_mapping.get("revenue", "revenue"), 0.0))
            })
            
        return jsonify({
            "success": True,
            "totalRows": len(df),
            "summary": {
                "channelCount": channel_count,
                "campaignCount": campaign_count,
                "totalSpend": total_spend
            },
            "errors": errors,
            "preview": preview_rows
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

